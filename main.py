import asyncio
import json

from aiocoap import GET, Context, Message


async def main():
    client = await Context.create_client_context()

    while True:
        try:
            request = Message(
                code=GET,
                uri="coap://127.0.0.1:5683/sensor/temperatura",
            )

            response = await client.request(request).response

            data = json.loads(response.payload.decode("utf-8"))

            print(f"Temperatura: {data['temperature']} °{data['unit']}")

        except Exception:  # noqa: BLE001
            print("No se pudo conectar con el servidor CoAP.")

        await asyncio.sleep(2)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente detenido.")
