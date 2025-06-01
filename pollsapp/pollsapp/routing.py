from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import polls_app.routing

application = ProtocolTypeRouter({
    # (http → Django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            polls_app.routing.websocket_urlpatterns
        )
    ),
})
