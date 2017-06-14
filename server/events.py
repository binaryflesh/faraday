from models import (
    Host,
    Service,
)
from sqlalchemy import event

from server.websocket_factories import changes_queue


def new_object_event(mapper, connection, instance):
    # Since we don't have jet a model for workspace we
    # retrieve the name from the connection string
    workspace_name = repr(connection.engine).split('.')[0].split('/')[-1]
    msg = {
        'id': instance.id,
        'action': 'CREATE',
        'type': instance.__class__.__name__,
        'name': instance.name,
        'workspace': workspace_name
    }
    changes_queue.put(msg)


def delete_object_event(mapper, connection, instance):
    workspace_name = repr(connection.engine).split('.')[0].split('/')[-1]
    msg = {
        'id': instance.id,
        'action': 'DELETE',
        'type': instance.__class__.__name__,
        'name': instance.name,
        'workspace': workspace_name
    }
    changes_queue.put(msg)


def update_object_event(mapper, connection, instance):
    workspace_name = repr(connection.engine).split('.')[0].split('/')[-1]
    msg = {
        'id': instance.id,
        'action': 'UPDATE',
        'type': instance.__class__.__name__,
        'name': instance.name,
        'workspace': workspace_name
    }
    changes_queue.put(msg)


# New object bindings
event.listen(Host, 'after_insert', new_object_event)
event.listen(Service, 'after_insert', new_object_event)

# Delete object bindings
event.listen(Host, 'after_delete', delete_object_event)
event.listen(Service, 'after_delete', delete_object_event)

# Update object bindings
event.listen(Host, 'after_update', update_object_event)
event.listen(Service, 'after_update', update_object_event)
