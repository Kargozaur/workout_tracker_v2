if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.workout.main:create_app",
        host="0.0.0.0",
        port=7000,
        loop="uvloop",
        reload=True,
        factory=True,
    )
