import asyncio
import json

from aiocoap import GET, Context, Message

RECONNECT_DELAY = 5
REQUEST_TIMEOUT = 3


async def main():
    client = await Context.create_client_context()

    while True:
        try:
            request = Message(
                code=GET,
                uri="coap://127.0.0.1:5683/sensor/temperatura",
            )

            response = await asyncio.wait_for(
                client.request(request).response,
                timeout=REQUEST_TIMEOUT,
            )

            data = json.loads(response.payload.decode("utf-8"))

            print(f"Temperatura: {data['temperature']} °{data['unit']}")

            await asyncio.sleep(2)

        except Exception:  # noqa: BLE001
            print("No se pudo conectar con el servidor CoAP.")

            await client.shutdown()

            print(f"Reintentando en {RECONNECT_DELAY} segundos...")

            await asyncio.sleep(RECONNECT_DELAY)

            client = await Context.create_client_context()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCliente detenido.")
