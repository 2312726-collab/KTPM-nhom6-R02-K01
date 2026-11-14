"""
Seed Data Script for Mealie - Dataset NAM (Nguyễn Phạm Phú Nam)
- Seeds 10 specialized recipes (NAM-01 to NAM-10)
- Configures 7-day meal plan (06/10/2026 to 12/10/2026)
- Idempotent: checks for existing recipes before creating to prevent duplicates
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = os.environ.get("MEALIE_BASE_URL", "http://localhost:9925")
EMAIL = os.environ.get("MEALIE_EMAIL", "admin@nhom6.test")
PASSWORD = os.environ.get("MEALIE_PASSWORD", "Admin123@")

def api_post(path, data, token=None, is_form=False):
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    if is_form:
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        encoded_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"POST {path} failed: {e.code} - {err_msg}")

def api_patch(path, data, token):
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    encoded_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"PATCH {path} failed: {e.code} - {err_msg}")

def api_get(path, token):
    url = f"{BASE_URL}{path}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        raise RuntimeError(f"GET {path} failed: {e.code} - {err_msg}")

def login():
    print(f"Logging in to {BASE_URL} as {EMAIL}...")
    resp = api_post("/api/auth/token", {"username": EMAIL, "password": PASSWORD}, is_form=True)
    return resp["access_token"]

unit_cache = {}
food_cache = {}

def get_or_create_unit(name, token):
    if not name:
        return None
    name_lower = name.lower()
    if name_lower in unit_cache:
        return unit_cache[name_lower]
    try:
        res = api_get(f"/api/units?query={urllib.parse.quote(name)}", token)
        for u in res.get("items", []):
            if u["name"].lower() == name_lower:
                unit_cache[name_lower] = u
                return u
        new_u = api_post("/api/units", {"name": name}, token=token)
        unit_cache[name_lower] = new_u
        return new_u
    except Exception:
        return None

def get_or_create_food(name, token):
    if not name:
        return None
    name_lower = name.lower()
    if name_lower in food_cache:
        return food_cache[name_lower]
    try:
        res = api_get(f"/api/foods?query={urllib.parse.quote(name)}", token)
        for f in res.get("items", []):
            if f["name"].lower() == name_lower:
                food_cache[name_lower] = f
                return f
        new_f = api_post("/api/foods", {"name": name}, token=token)
        food_cache[name_lower] = new_f
        return new_f
    except Exception:
        return None

def parse_ingredient(ing_text, token):
    try:
        res = api_post("/api/parser/ingredient", {"ingredient": ing_text}, token=token)
        ing = res.get("ingredient", {})
        qty = ing.get("quantity")
        note = ing.get("note") or ""
        display = ing.get("display") or ing_text
        unit_name = ing.get("unit", {}).get("name") if ing.get("unit") else None
        food_name = ing.get("food", {}).get("name") if ing.get("food") else None

        unit_obj = get_or_create_unit(unit_name, token) if unit_name else None
        food_obj = get_or_create_food(food_name, token) if food_name else None

        return {
            "quantity": qty,
            "note": note,
            "display": display,
            "unit": unit_obj,
            "food": food_obj,
            "originalText": ing_text
        }
    except Exception:
        return {
            "quantity": None,
            "note": ing_text,
            "display": ing_text,
            "unit": None,
            "food": None,
            "originalText": ing_text
        }

def seed_recipes(token):
    seed_file = os.path.join(os.path.dirname(__file__), "recipes_nam.json")
    with open(seed_file, "r", encoding="utf-8") as f:
        recipes_data = json.load(f)

    # Get existing recipes
    existing_resp = api_get("/api/recipes?perPage=100", token)
    existing_items = existing_resp.get("items", [])
    existing_map = {r["name"]: r["slug"] for r in existing_items}

    seeded_recipes = {}

    for item in recipes_data:
        name = item["name"]
        print(f"Processing recipe: {name}...")

        if name in existing_map:
            slug = existing_map[name]
            print(f"  -> Already exists with slug: {slug}")
        else:
            slug = api_post("/api/recipes", {"name": name}, token=token)
            print(f"  -> Created with slug: {slug}")
            existing_map[name] = slug

        # Parse ingredients using Mealie parser
        parsed_ingredients = []
        for ing_str in item["ingredients"]:
            parsed = parse_ingredient(ing_str, token)
            parsed_ingredients.append(parsed)

        instructions = [{"text": step} for step in item["instructions"]]

        patch_payload = {
            "description": item["description"],
            "recipeServings": float(item["recipeServings"]),
            "recipeYield": item["recipeYield"],
            "recipeIngredient": parsed_ingredients,
            "recipeInstructions": instructions
        }

        updated = api_patch(f"/api/recipes/{slug}", patch_payload, token)
        seeded_recipes[item["id"]] = updated
        print(f"  -> Updated recipe details (ID: {updated['id']})")

    return seeded_recipes

def seed_meal_plan(token, seeded_recipes):
    print("\nSetting up 7-day Meal Plan (06/10/2026 - 12/10/2026)...")

    # Check existing meal plans
    existing_plans = api_get("/api/households/mealplans?perPage=100", token)
    existing_items = existing_plans.get("items", [])
    existing_dates = {(p["date"], p["entryType"]): p["id"] for p in existing_items}

    plan_entries = [
        {"date": "2026-10-06", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-01"]["id"], "title": "Bữa sáng ngày 06/10"},
        {"date": "2026-10-06", "entryType": "dinner", "recipeId": seeded_recipes["NAM-02"]["id"], "title": "Bữa tối ngày 06/10"},

        {"date": "2026-10-07", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-03"]["id"], "title": "Bữa sáng ngày 07/10"},
        {"date": "2026-10-07", "entryType": "dinner", "recipeId": seeded_recipes["NAM-08"]["id"], "title": "Bữa tối ngày 07/10"},

        {"date": "2026-10-08", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-04"]["id"], "title": "Bữa sáng ngày 08/10"},
        {"date": "2026-10-08", "entryType": "dinner", "recipeId": seeded_recipes["NAM-05"]["id"], "title": "Bữa tối ngày 08/10"},

        {"date": "2026-10-09", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-06"]["id"], "title": "Bữa sáng ngày 09/10"},
        {"date": "2026-10-09", "entryType": "dinner", "recipeId": seeded_recipes["NAM-10"]["id"], "title": "Bữa tối ngày 09/10"},

        {"date": "2026-10-10", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-07"]["id"], "title": "Bữa sáng ngày 10/10"},
        {"date": "2026-10-10", "entryType": "dinner", "recipeId": seeded_recipes["NAM-09"]["id"], "title": "Bữa tối ngày 10/10"},

        {"date": "2026-10-11", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-01"]["id"], "title": "Bữa sáng ngày 11/10"},
        {"date": "2026-10-11", "entryType": "dinner", "recipeId": seeded_recipes["NAM-10"]["id"], "title": "Bữa tối ngày 11/10"},

        {"date": "2026-10-12", "entryType": "breakfast", "recipeId": seeded_recipes["NAM-02"]["id"], "title": "Bữa sáng ngày 12/10"},
        {"date": "2026-10-12", "entryType": "dinner", "recipeId": seeded_recipes["NAM-03"]["id"], "title": "Bữa tối ngày 12/10"},
    ]

    for p in plan_entries:
        key = (p["date"], p["entryType"])
        if key in existing_dates:
            print(f"  -> Meal plan on {p['date']} ({p['entryType']}) already exists.")
            continue
        created = api_post("/api/households/mealplans", p, token=token)
        print(f"  -> Created meal plan on {p['date']} ({p['entryType']}): {p['title']}")

def main():
    token = login()
    seeded = seed_recipes(token)
    seed_meal_plan(token, seeded)
    print("\nSeed data completed successfully!")

if __name__ == "__main__":
    main()
