"""Infrastructure layer: adapters that implement the application ports with real tools.

This is the only layer that talks to Ollama, files, Windows, the microphone,
Google Calendar and so on. Swap an adapter without touching the use cases.
"""
