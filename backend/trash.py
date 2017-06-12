import datetime
import enum
import typing

import core.api


class Sorting(enum.IntFlag):
    """Enum used for specifying what sorting mode
    should be used for functions.
    """
    date = enum.auto()
    date_reversed = enum.auto()
    date_moved_to_trash = enum.auto()
    date_moved_to_trash_reversed = enum.auto()


def _get_trash_items_raw() -> typing.Iterator[typing.Tuple[str, dict]]:
    """Return an iterator over all items which have been moved
    to trash as (uuid, data) tuples.
    """
    for uuid, appointment in core.api.get_var('appointments').items():
        if appointment['in_trash']:
            yield uuid, appointment

_t = typing.Iterator[typing.Tuple[str, dict]]


def get_trash_items(sort_by: Sorting = Sorting.date_moved_to_trash) -> _t:
    """Return an iterator over all items which have been moved to
    trash as (uuid, data) tuples in sorted order.

    `sort_by`: Flag to indicate how the appointments should
                be sorted. Should be a member of the
                'Sorting' enum.

    - Raise ValueError when invalid sorting mode is passed.
    """
    if sort_by == Sorting.date:
        yield from sorted(_get_trash_items_raw().items(),
                          key=lambda app: app[0]['from'])
    elif sort_by == Sorting.date:
        yield from sorted(_get_trash_items_raw().items(),
                          key=lambda app: app[0]['from'],
                          reverse=True)
    elif sort_by == Sorting.date_moved_to_trash:
        yield from sorted(_get_trash_items_raw().items(),
                          key=lambda app: app[0]['moved_to_trash'])
    elif sort_by == Sorting.date_moved_to_trash_reversed:
        yield from sorted(_get_trash_items_raw().items(),
                          key=lambda app: app[0]['moved_to_trash'],
                          reverse=True)
    else:
        raise ValueError(f'Invalid sorting mode {sort_by!r}')

del _t


def clear_trash(expiration_time=datetime.timedelta(seconds=0)):
    """Remove all items which have been in trash for at least
    'expiration_time'. Defaults to all appointments.

    `expiration_time`: datetime.timedelta indicating the time
                        span for which the appointment should
                        have been in trash.
    """
    now = datetime.datetime.now()
    to_remove = (
        uuid for uuid, appointment in _get_trash_items_raw()
        if now - appointment['moved_to_trash'] >= expiration_time)
    appointments = core.api.get_var('appointments')
    for uuid in to_remove:
        del appointments[uuid]
    # Save changes
    core.api.call('save', core.api.get_var('DATA_FILE'), appointments)


def move_to_trash(uuid: str):
    """Move the appointment corresponding to the given uuid
    to trash and set trash_history_id equal to this uuid.

    `uuid`: UUID of the appointment.

    - Raise LookupError when no appointment corresponding
        to the uuid can be found.
    - Raise ValueError if the appointment was already
        moved to trash
    """
    try:
        appointment = core.api.get_var('appointments')[uuid]
    except KeyError:
        raise LookupError(f'No appointment with uuid {uuid!r} exits')
    if appointment['in_trash']:
        msg = (f'appointment with uuid {uuid!r} has already'
               ' been moved to trash')
        raise ValueError(msg)
    appointment['in_trash'] = True
    appointment['moved_to_trash'] = datetime.now().timestamp()
    core.api.set_var('trash_history_id', uuid)


def move_from_trash(uuid: str):
    """Move the appointment corresponding to the
    given uuid from the trash and clear trash_history_id
    if the value is equal to the given uuid.

    `uuid`: UUID of the appointment.

    - Raise LookupError when no appointment corresponding
        to the uuid can be found.
    - Raise ValueError if the appointment corresponding
        to the uuid is not in the trashcan.
    """
    try:
        appointment = core.api.get_var('appointments')[uuid]
    except KeyError:
        raise LookupError(f'No appointment with uuid {uuid!r} exits')
    if not appointment['in_trash']:
        msg = (f'appointment with uuid {uuid!r} is not'
               ' in the trash')
        raise ValueError(msg)
    appointment['in_trash'] = False
    appointment['moved_to_trash'] = -1
    if core.api.get_var('trash_history_id') == uuid:
        core.api.set_var('trash_history_id', None)


# Initialize trash_history_id
core.api.set_var('trash_history_id', None )
