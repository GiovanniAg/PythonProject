from sanic import Sanic
from sanic.response import text
from config.env import env

from api import product_api


app = Sanic(__name__)
app.config.OAS_UI_DEFAULT = "swagger"
app.config.OAS_UI_REDOC = False


@app.get("/health", name="health")
async def health(req):
    return text("Ok", 200)


app.blueprint(product_api.blueprint, url_prefix="products")


if __name__ == "__main__":
    app.run(
        host=env.server_host,
        port=env.server_port,
        debug=env.is_dev,
        auto_reload=env.is_dev
    )