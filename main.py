 from fastapi import FastAPI
  from pydantic import BaseModel
  from datetime import date
  from cep import Transferencia
  from cep.exc import TransferNotFoundError

  app = FastAPI()

  class Pago(BaseModel):
      fecha: str
      clave_rastreo: str
      emisor: str
      receptor: str
      cuenta: str
      monto: float

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
          return {"encontrada": True, "transferencia": vars(t)}
      except TransferNotFoundError:
          return {"encontrada": False, "mensaje": "No encontrada en Banxico"}
