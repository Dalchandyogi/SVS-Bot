import whatsapp_utils as whatsapp
import asyncio

import logging

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)

components = [
    {
        "type": "body",
        "parameters": [
            {"type": "text", "text": "123456"} 
        ]
    }
]

async def main():
    await whatsapp.send_template(
        to_number="916378533897",
        template_name="otp",
        language="en_US",
        components=components
    )

asyncio.run(main())
