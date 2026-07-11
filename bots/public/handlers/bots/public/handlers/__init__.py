from .start import router as start_router
# Adicione outros routers aqui

def setup_public_handlers(dp):
    dp.include_router(start_router)
    # dp.include_router(others...)
