from fastapi import FastAPI                                                                    from pydantic import BaseModel                                                                 from datetime import date                                                                      from cep import Transferencia                                                                  from cep.exc import TransferNotFoundError

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

class Pago(BaseModel):
    fecha: str
    clave_rastreo: str
    emisor: str
    receptor: str
    cuenta: str
    monto: float

def cuenta_to_dict(c):
    return {
        "nombre": c.nombre,
        "tipo_cuenta": c.tipo_cuenta,
        "banco": c.banco,
        "numero": c.numero,
        "rfc": c.rfc,
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validar")
def validar(pago: Pago):
    try:
        t = Transferencia.validar(
            fecha=date.fromisoformat(pago.fecha),
            clave_rastreo=pago.clave_rastreo,
            emisor=pago.emisor,
            receptor=pago.receptor,
            cuenta=pago.cuenta,
            monto=int(pago.monto * 100)
        )
        return {
            "encontrada": True,
            "transferencia": {
                "fecha_operacion": str(t.fecha_operacion),
                "fecha_abono": str(t.fecha_abono),
                "monto_pesos": float(t.monto_pesos),
                "concepto": t.concepto,
                "clave_rastreo": t.clave_rastreo,
                "tipo_pago": t.tipo_pago,
                "ordenante": cuenta_to_dict(t.ordenante),
                "beneficiario": cuenta_to_dict(t.beneficiario),
            }
        }
    except TransferNotFoundError:
        return {"encontrada": False, "mensaje": "No encontrada en Banxico"}
