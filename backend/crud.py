
from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime
import random

def get_devices(db: Session):
    return db.query(models.Device).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(
        name=device.name,
        type=device.type or 'Server',
        status=device.status or 'Pending',
        recovery_percent=device.recovery_percent or 0.0,
        details=device.details or '',
        last_checked=datetime.utcnow()
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def delete_all_devices(db: Session):
    db.query(models.Device).delete()
    db.commit()

def create_sample_devices(db: Session):
    samples = [
        ('DB-Primary', 'Database'),
        ('App-Server-1', 'Application'),
        ('Web-Gateway', 'Network'),
        ('Backup-System', 'Storage'),
        ('Auth-Service', 'Application')
    ]
    for name, typ in samples:
        d = models.Device(
            name=name,
            type=typ,
            status=random.choice(['Recovered','In Progress','Failed','Pending']),
            recovery_percent=round(random.uniform(10,100),2)
        )
        db.add(d)
    db.commit()

def recovery_summary(db: Session):
    devices = db.query(models.Device).all()
    if not devices:
        return {'count':0, 'avg_recovery':0.0}
    count = len(devices)
    avg = sum((d.recovery_percent or 0) for d in devices)/count
    status_counts = {}
    for d in devices:
        status_counts[d.status] = status_counts.get(d.status,0)+1
    return {
        'count': count,
        'avg_recovery': round(avg,2),
        'status_counts': status_counts
    }
