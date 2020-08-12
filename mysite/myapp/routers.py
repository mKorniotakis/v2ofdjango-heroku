from myapp.models import Measurements

class legacyDB(object):

    def db_for_read(self, model, **hints):
        if model == Measurements:
            return 'legacyDB'
        # Returning None is no opinion, defer to other routers or default database
        return None
    def db_for_write(self, model, **hints):
        if model == Measurements:
            return 'legacyDB'
         # Returning None is no opinion, defer to other routers or default database
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the Example app's models get created on the right database."""
        if model_name == 'measurements':
            # The model measurements should be migrated only on the legacyDB database.
            return db == 'legacyDB'
        elif db == 'legacyDB':
            # Ensure that all other models don't get migrated on the legacyDB database.
            return False

        # No opinion for all other scenarios
        return None