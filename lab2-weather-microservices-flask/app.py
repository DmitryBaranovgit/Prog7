from services.weather_service import app as weather_app
from services.recommendation_service import app as rec_app
from services.history_service import app as hist_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

application = DispatcherMiddleware(weather_app, {
    "/recommendation": rec_app,
    "/history": hist_app,
})