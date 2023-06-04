# 


-> domain -> usecase -> repository -> interface (http)

Clean Architecture, a concept popularized by Robert C. Martin (also known as Uncle Bob), 
is a design principle aimed at creating systems that are independent of frameworks, UI, databases, and external agencies. 
This ensures the system is highly maintainable, flexible, and testable.

Here is a brief rundown of its major elements:

    Independent of Frameworks: The architecture does not depend on the existence of specific tools, libraries, or frameworks. It should be able to work with and without them.

    Testable: The business rules can be tested without the UI, database, web server, or any other external element.

    Independent of UI: The UI can change without changing the rest of the system. A web UI could be replaced with a console UI, for example, and the business rules would not need to change.

    Independent of Database: Your business rules are not bound to the database. You can swap out MySQL for MongoDB and your business rules should still work as expected.

    Independent of any external agency: Business rules don’t know anything at all about the outside world.

The architecture follows certain layers:

    Entities: These encapsulate Enterprise-wide business rules. An entity can be an object with methods, or it can be a set of data structures and functions.

    Use Cases: These encapsulate application-specific business rules. They orchestrate the interaction of entities to achieve a specific business goal.

    Interface Adapters: These convert data from the format most convenient for use cases and entities, to the format convenient for things like the web, database, UI, etc.

    Frameworks and Drivers: This is where all the details go. The web is a detail. The database is a detail. We keep these things on the outside where they can do little harm.

In the center of this architecture is the domain, where the entities and use cases reside. The outer layers communicate with the inner ones via interfaces (ports), and the inner layers don't know anything about the outer ones. The dependency rule states that dependencies must always point inwards, from outer layers to inner ones.

By applying Clean Architecture, you achieve separation of concerns, make the system easier to understand and maintain, and decouple it from technology-specific details.











```python
api_routes_bp.route("/api/pets", methods=["GET"])
def finder_pets():
    """ find pets route """

    message = {}
    response = flask_adapter(request=request, api_route=find_pet_composer())

    if response.status_code < 300:
        message = []

        for element in response.body:
            message.append(
                {
                    "type": "pets",
                    "id": element.id,
                    "attributest": {
                        "name": element.name,
                        "specie": element.specie.value,
                        "age": element.age,
                    },
                    "relationships": {
                        "owner": {"type": "users", "id": element.user_id}
                    },
                }
            )

        return jsonify({"data": message}), response.status_cod

```







