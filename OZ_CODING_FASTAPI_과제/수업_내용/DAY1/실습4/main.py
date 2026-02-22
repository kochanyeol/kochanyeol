from fastapi import FastAPI

app = FastAPI()

items = ["item1", "item2", "item3"]
@app.get("/order/{order_id}/")
def get_user(order_id: int, show_items: bool = False):
    if not show_items:
        return {"order_id": order_id}
    else:
        return {"order_id": order_id, "items": items}


# {order_id}는 경로변수이고, show_items는 쿼리변수이다.