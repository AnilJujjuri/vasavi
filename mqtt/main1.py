import uvicorn
from apps import apps


if __name__ == "__main__":
    uvicorn.run(apps, host='localhost', port=8884)

