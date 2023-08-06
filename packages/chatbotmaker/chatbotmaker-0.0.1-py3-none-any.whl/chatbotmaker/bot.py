""" Bot class file """
from . import ExtendedUser


class Bot:
    """ Class represents abstract bot who interacts with the user """

    def __init__(self, config: dict, messenger, dispatcher, database):
        self.config = config
        self.messenger = messenger
        self.dispatcher = dispatcher
        self.database = database

    def user_handle(self, user_id: str, user_input: str) -> str:
        """ An implementation of the user_handle """
        session = self.database.session()
        User = self.database.user_class
        # Get or Create the user
        req = session.query(User).filter(User.fb_id == user_id)
        user = req.scalar()
        if not user:
            user = User(fb_id=user_id, state='welcome')
            session.add(user)
            session.commit()

        # extend the user
        ext_user = ExtendedUser(user, self.messenger, self.dispatcher,
                                self.database)
        ext_user.mark_seen()
        # call the handle
        ext_user.execute_handle(user_input)

        session.commit()
        session.close()

        return f'{user_id}\'s request has been handled'
