import json

from firebase_functions import https_fn

from firestore_client import get_firestore_client


@https_fn.on_request()
def get_user_stores_http(request):
    db = get_firestore_client()
    try:
        if request.method != 'POST':
            return json.dumps({"error": "Only POST method is allowed."}), 405, {'Content-Type': 'application/json'}
        try:
            data = request.get_json(force=True)
        except Exception:
            return json.dumps({"error": "Invalid JSON body."}), 400, {'Content-Type': 'application/json'}
        user_id = data.get('userId')
        if not user_id:
            return json.dumps({"error": "Missing 'userId' parameter."}), 400, {'Content-Type': 'application/json'}
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        if not user_doc.exists:
            return json.dumps({"error": "User not found."}), 404, {'Content-Type': 'application/json'}
        user_data = user_doc.to_dict() or {}
        stores = user_data.get('stores', [])
        full_stores = []
        for store in stores:
            store_id = store.get('id')
            role = store.get('role')
            if store_id:
                store_ref = db.collection('stores').document(store_id)
                store_doc = store_ref.get()
                if store_doc.exists:
                    store_data = store_doc.to_dict()
                    store_data['id'] = store_id
                    store_data['role'] = role
                    full_stores.append(store_data)

        def firestore_json_default(obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        stores_json = json.dumps({"stores": full_stores}, default=firestore_json_default)
        return stores_json, 200, {'Content-Type': 'application/json'}
    except Exception as exc:
        return json.dumps({"error": f"Internal server error: {str(exc)}"}), 500, {'Content-Type': 'application/json'}
