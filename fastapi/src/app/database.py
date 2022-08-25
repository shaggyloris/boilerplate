from .schemas import UserInDB, NewUser

class DemoDB:
    """
    Not a real database, just used to demonstrate functionality.
    Note: Hashed password is not secure and just being used for example purposes. Password is mysupersecretpassword
    """
    data = {
        "users": {
            "demo_user": {
                "username": "demo_user",
                "hashed_password": "$2b$12$Lt.jWahGYHFPqnVzOEzh0.3M8xJKHj/7lHG7YtWAC4Q4dRSRExl/K"
                }
            }
        }
    def __init__(self):
        ...
    
    def get_user(self, username: str) -> UserInDB:
        user = self.data["users"].get(username)
        if user:
            user = UserInDB(**user)
        return user
        
    def add_user(self, user: UserInDB) -> None:
        if user.username in self.data.get("users"):
            raise ValueError(f"User {user.username} already exists!")
        self.data["users"][user.username] = user.dict()
    
    
    def close(self):
        ...



async def get_db():
    db = DemoDB()
    try:
        yield db
    finally:
        db.close()
