from firebase_admin import initialize_app, firestore


def get_firestore_client():
    global firebase_app, db
    if not globals().get('firebase_app'):
        globals()['firebase_app'] = initialize_app()
    if not globals().get('db'):
        globals()['db'] = firestore.client()
    return globals()['db']

