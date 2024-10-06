import asyncio
from langchain_community.document_loaders import PyPDFLoader

async def load_pdf():
    loader = PyPDFLoader("/Users/USER_ADMIN/Desktop/Resume for Techincal jobs/Melika El Wadany v2.33.pdf")
    pages = []
    
    async for page in loader.alazy_load():
        pages.append(page)
    
    print(f"{pages[1].metadata}\n")
    print(pages[0].page_content)

# Run the asynchronous function
asyncio.run(load_pdf())
