import json
import random
from faker import Faker

fake = Faker("en_US")
random.seed(42)


# --- generators ---

def make_israeli_id():
    digits = [random.randint(0, 9) for _ in range(8)]
    total = sum(d * 2 - 9 if d * (1 + i % 2) > 9 else d * (1 + i % 2) for i, d in enumerate(digits))
    check = (10 - (total % 10)) % 10
    return "".join(map(str, digits)) + str(check)


def make_phone():
    prefix = random.choice(["050", "052", "053", "054", "058", "+972-50", "+972-52"])
    number = "".join([str(random.randint(0, 9)) for _ in range(7)])
    sep = random.choice(["-", ""])
    return f"{prefix}{sep}{number}"


def make_credit_card():
    digits = [4, 1, 1, 1] + [random.randint(0, 9) for _ in range(11)]
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 0:
            x = d * 2
            total += x - 9 if x > 9 else x
        else:
            total += d
    check = (10 - (total % 10)) % 10
    digits.append(check)
    groups = ["".join(map(str, digits[i:i+4])) for i in range(0, 16, 4)]
    sep = random.choice(["-", " ", ""])
    return sep.join(groups)


# --- templates ---


SINGLE_ENTITY_TEMPLATES = [
    ("My name is {name}.", [("PERSON", "{name}")]),
    ("Contact {name} for more information.", [("PERSON", "{name}")]),
    ("The employee {name} submitted the report.", [("PERSON", "{name}")]),
    ("Please call {phone}.", [("PHONE_NUMBER", "{phone}")]),
    ("You can reach us at {phone} during business hours.", [("PHONE_NUMBER", "{phone}")]),
    ("Send your resume to {email}.", [("EMAIL", "{email}")]),
    ("For support, email {email}.", [("EMAIL", "{email}")]),
    ("The ID number is {id}.", [("ISRAELI_ID", "{id}")]),
    ("Verify using ID {id}.", [("ISRAELI_ID", "{id}")]),
    ("Charge the amount to card {card}.", [("CREDIT_CARD", "{card}")]),
    ("Payment was made with {card}.", [("CREDIT_CARD", "{card}")]),
    ("The meeting is in {city}.", [("LOCATION", "{city}")]),
    ("Our office is located in {city}.", [("LOCATION", "{city}")]),
    ("The contract was signed on {date}.", [("DATE", "{date}")]),
]

MULTI_ENTITY_TEMPLATES = [
    ("My name is {name} and my ID is {id}.", [("PERSON", "{name}"), ("ISRAELI_ID", "{id}")]),
    ("Contact {name} at {email}.", [("PERSON", "{name}"), ("EMAIL", "{email}")]),
    ("Call {name} at {phone}.", [("PERSON", "{name}"), ("PHONE_NUMBER", "{phone}")]),
    ("My name is {name}, email {email}, phone {phone}.", [("PERSON", "{name}"), ("EMAIL", "{email}"), ("PHONE_NUMBER", "{phone}")]),
    ("{name} will attend the meeting in {city}.", [("PERSON", "{name}"), ("LOCATION", "{city}")]),
    ("On {date}, {name} paid with card {card}.", [("DATE", "{date}"), ("PERSON", "{name}"), ("CREDIT_CARD", "{card}")]),
    ("Please verify ID {id} for {name}, reachable at {email}.", [("ISRAELI_ID", "{id}"), ("PERSON", "{name}"), ("EMAIL", "{email}")]),
    ("{name} is based in {city}.", [("PERSON", "{name}"), ("LOCATION", "{city}")]),
    ("Send the invoice to {email} and call {phone} to confirm.", [("EMAIL", "{email}"), ("PHONE_NUMBER", "{phone}")]),
    ("{name} ID {id} paid {card} on {date}.", [("PERSON", "{name}"), ("ISRAELI_ID", "{id}"), ("CREDIT_CARD", "{card}"), ("DATE", "{date}")]),
]

EDGE_CASE_TEMPLATES = [
    ("Send an email to{email}.", [("EMAIL", "{email}")]),
    ("The ID:{id} belongs to {name}.", [("ISRAELI_ID", "{id}"), ("PERSON", "{name}")]),
    ("({phone}) is the emergency line.", [("PHONE_NUMBER", "{phone}")]),
    ("Card number: {card}.", [("CREDIT_CARD", "{card}")]),
    ("{name}'s account was flagged.", [("PERSON", "{name}")]),
    ("Reach out to {name} ({email}).", [("PERSON", "{name}"), ("EMAIL", "{email}")]),
    ("Born on {date} in {city}.", [("DATE", "{date}"), ("LOCATION", "{city}")]),
    ("The suspect, {name}, lives in {city} and can be reached at {phone}.", [("PERSON", "{name}"), ("LOCATION", "{city}"), ("PHONE_NUMBER", "{phone}")]),
    ("Billing: {card} — Contact: {email}", [("CREDIT_CARD", "{card}"), ("EMAIL", "{email}")]),
    ("{name}: {phone}", [("PERSON", "{name}"), ("PHONE_NUMBER", "{phone}")]),
    ("ID={id}", [("ISRAELI_ID", "{id}")]),
    ("[{name}] submitted form, ID {id}.", [("PERSON", "{name}"), ("ISRAELI_ID", "{id}")]),
]

HEBREW_PREFIX_TEMPLATES = [
    ("The message was sent to{name} yesterday.", [("PERSON", "{name}")]),
    ("We received confirmation from{name}.", [("PERSON", "{name}")]),
    ("Reply was sent to{email} automatically.", [("EMAIL", "{email}")]),
    ("An alert was triggered for{name} account.", [("PERSON", "{name}")]),
]

NEGATIVE_TEMPLATES = [
    "Please review the attached document.",
    "Our performance metrics exceeded expectations.",
    "The new policy will take effect immediately.",
    "The server was updated successfully.",
    "All team members should attend the standup.",
    "The budget has been approved.",
    "The deployment was successful.",
    "Please review the pull request.",
    "The infrastructure migration is complete.",
    "Access permissions have been updated.",
    "The configuration file was modified.",
    "The build pipeline completed without errors.",
    "Documentation has been updated in the repository.",
    "The feature request was approved by the team.",
    "Code review comments have been addressed.",
]


# --- builder ---

def fill_template(template, entity_defs):
    values = {
        "{name}": fake.name(),
        "{city}": fake.city(),
        "{date}": fake.date_this_decade().strftime("%B %d, %Y"),
        "{phone}": make_phone(),
        "{email}": fake.email(),
        "{id}": make_israeli_id(),
        "{card}": make_credit_card(),
    }

    text = template
    entities = []
    for entity_type, placeholder in entity_defs:
        value = values[placeholder]
        text = text.replace(placeholder, value, 1)
        entities.append({"type": entity_type, "value": value})

    return {"text": text, "entities": entities}


def build_dataset():
    dataset = []
    idx = 0

    for _ in range(10):
        for template, entity_defs in SINGLE_ENTITY_TEMPLATES:
            entry = fill_template(template, entity_defs)
            entry["id"] = f"single_{idx}"
            entry["category"] = "single_entity"
            dataset.append(entry)
            idx += 1

    for _ in range(15):
        for template, entity_defs in MULTI_ENTITY_TEMPLATES:
            entry = fill_template(template, entity_defs)
            entry["id"] = f"multi_{idx}"
            entry["category"] = "multi_entity"
            dataset.append(entry)
            idx += 1

    for _ in range(20):
        for template, entity_defs in EDGE_CASE_TEMPLATES:
            entry = fill_template(template, entity_defs)
            entry["id"] = f"edge_{idx}"
            entry["category"] = "edge_case"
            dataset.append(entry)
            idx += 1

    for _ in range(25):
        for template, entity_defs in HEBREW_PREFIX_TEMPLATES:
            entry = fill_template(template, entity_defs)
            entry["id"] = f"heb_{idx}"
            entry["category"] = "hebrew_prefix"
            dataset.append(entry)
            idx += 1

    for i, template in enumerate(NEGATIVE_TEMPLATES * 15):
        dataset.append({
            "id": f"neg_{i}",
            "category": "negative",
            "text": template,
            "entities": []
        })

    random.shuffle(dataset)
    return dataset


if __name__ == "__main__":
    dataset = build_dataset()
    with open("dataset.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(dataset)} examples")
    cats = {}
    for d in dataset:
        cats[d["category"]] = cats.get(d["category"], 0) + 1
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")
