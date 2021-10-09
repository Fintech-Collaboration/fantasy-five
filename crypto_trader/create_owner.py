import manage

from sandbox.models import Owner


def create_owner_database():
    usernames   = ["mbejan35", "jasonjgarcia24", "sngoda", "saeedraghib02"]
    first_names = ["Michael" , "Jason"         , "Srini" , "Saeed"]
    last_names  = ["Bejan"   , "Garcia"        , "Goda"  , "Ali Raghib"]
    emails       = [
        "Mbejan@scu.edu",
        "jason.garcia24@gmail.com",
        "sngoda@hotmail.com",
        "saeed_raghib@msn.com"
        ]


    for username, first_name, last_name, email in zip(usernames, first_names, last_names, emails):
        this_owner = Owner(username=username, first_name=first_name, last_name=last_name, email=email)
        this_owner.save()

    if __name__ == "__main__":
        create_owner_database()

