import sys

import decouple
import uvicorn
if __name__ == '__main__':
    app_port = int(8000)
    sys.path.insert(0, '')
    uvicorn.run("src.app:app", port=app_port, host='127.0.0.1', reload=True)