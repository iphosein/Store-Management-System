from sqlalchemy.orm import Session
from .. import models
from sqlalchemy import func , distinct


def get_report (db : Session , from_time, to_time):

    query = db.query(models.Invoice).filter(models.Invoice.purchase_date <= to_time , models.Invoice.purchase_date >= from_time)

    invoices_count = query.count()

    total_paid = db.query(func.coalesce(func.sum(models.Invoice.total_paid), 0)).filter(
        models.Invoice.purchase_date <= to_time , models.Invoice.purchase_date >= from_time
    ).scalar()

    average_paid = total_paid / invoices_count if invoices_count > 0 else 0

    customers_count = (
        db.query(func.count(distinct(models.Invoice.customer_id)))
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .scalar()
    )

    max_paid_invoice = (
        db.query(models.Invoice.id , models.Invoice.customer_id, models.Invoice.total_paid)
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .order_by(models.Invoice.total_paid.desc())
        .first()
    )

    min_paid_invoice = (
        db.query(models.Invoice.id, models.Invoice.customer_id, models.Invoice.total_paid)
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .order_by(models.Invoice.total_paid.asc())
        .first()
    )

    #Id & count of paid
    best_customer = (
        db.query(
            models.Invoice.customer_id,
            func.sum(models.Invoice.total_paid).label("total_paid")
        )
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .group_by(models.Invoice.customer_id)
        .order_by(func.sum(models.Invoice.total_paid).desc())
        .first()
    )

    total_items = (
        db.query(func.coalesce(func.sum(models.InvoiceItem.quantity), 0))
        .join(models.Invoice)
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .scalar()
    )

    average_item_invoice = (
        total_items / invoices_count
        if invoices_count > 0 else 0
    )

    most_sold_product = (
        db.query(
            models.InvoiceItem.product_id,
            func.sum(models.InvoiceItem.quantity).label("total_sold")
        )
        .join(models.Invoice)
        .filter(
            models.Invoice.purchase_date >= from_time,
            models.Invoice.purchase_date <= to_time
        )
        .group_by(models.InvoiceItem.product_id)
        .order_by(func.sum(models.InvoiceItem.quantity).desc())
        .first()
    )

    max_paid = (
        {
            "invoice_id": max_paid_invoice.id,
            "customer_id": max_paid_invoice.customer_id,
            "total_paid": float(max_paid_invoice.total_paid)
        }
        if max_paid_invoice else None
    )

    min_paid = (
        {
            "invoice_id": min_paid_invoice.id,
            "customer_id": min_paid_invoice.customer_id,
            "total_paid": float(min_paid_invoice.total_paid)
        }
        if min_paid_invoice else None
    )

    best_customer_data = (
        {
            "customer_id": best_customer.customer_id,
            "total_paid": float(best_customer.total_paid)
        }
        if best_customer else None
    )

    most_sold_product_data = (
        {
            "product_id": most_sold_product.product_id,
            "total_sold": float(most_sold_product.total_sold)
        }
        if most_sold_product else None
    )

    return {
        "invoices_count": invoices_count,
        "total_paid": float(total_paid),
        "average_paid": float(average_paid),
        "customers_count": customers_count,
        "max_paid": max_paid,
        "min_paid": min_paid,
        "best_customer": best_customer_data,
        "average_item_invoice": float(average_item_invoice),
        "most_sold_product": most_sold_product_data
    }
