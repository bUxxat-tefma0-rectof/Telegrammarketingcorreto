from .start import router as start_router
from .plans import router as plans_router
# Adicione mais handlers aqui no futuro

def setup_public_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(plans_router)
    # dp.include_router(support_router) etc.
