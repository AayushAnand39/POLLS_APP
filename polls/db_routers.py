class PollsRouter:
    """
    A router to control all database operations on models for polls and voting.
    Models: Poll, PollOption, Vote will go to 'polls_db'.
    PollHistory and Profile (and any auth models) remain in 'default'.
    """
    
    poll_models = {'poll', 'polloption', 'vote'}

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.poll_models:
            return 'polls_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.poll_models:
            return 'polls_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.model_name in self.poll_models or
            obj2._meta.model_name in self.poll_models
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.poll_models:
            return db == 'polls_db'
        return db == 'default'