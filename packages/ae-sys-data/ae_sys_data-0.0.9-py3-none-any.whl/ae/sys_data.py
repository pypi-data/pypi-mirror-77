"""
external system data structures
===============================

This module allows your application to easily manage data structures for to interface data flows
from and onto other/external systems.

A external system can be nearly anything: like e.g.: a database or web server or
an application or software suite with an interface for data exchanges; even data files
can be used as an external system.

The same data can be represented differently on different systems. This module allows you
to specify individual data structures for each system and provides hooks for to easily integrate
system-specific data conversion functions.


data structures
---------------

Use the classes of this module for to define any kind of simple data structures - like lists, mappings and trees:

* A list can get represented by a instance of one of the classes :class:`Records` or :class:`Values`. Each
  :class:`Records` instance is a sequence of 0..n :class:`Record` instances. A :class:`Values` instance
  is a sequence of 1..n :class:`Value` instances.
* A mapping get represented by an instance of the class :class:`Record`, whereas each mapping item gets
  represented by an instance of the private class :class:`_Field`.
* A node of a tree structure can be represented by an instance of the classes :class:`Values`, :class:`Records` or
  :class:`Record`.

By combining these simple data structures you can build any complex data structures.
The root of such a complex data structure can be defined by an instance of either :class:`Records` or :class:`Record`.

The leaves of any simple or complex data structure are represented by instances of the :class:`Value` class.

The following diagram is showing a complex data structure with all the possible combinations (of a single system):

.. graphviz::

    digraph {
        node [shape=record]
        rec1 [label="{<rec1>Record (root) | { <A>Field A | <B>Field B | <C>Field C | <D>Field D } }"]
        "Records (root)" -> rec1 [arrowhead=crow style=tapered penwidth=3]
        rec1:A -> "Value (of Field A)" [minlen=3]
        rec1:B -> "Values"
        "Values" -> "Value (of one Values item)" [minlen=2 arrowhead=crow style=tapered penwidth=3]
        rec2 [label="{<rec2>Record (sub-record) | { <CA>Field CA | <CB>Field CB | <CN>... } }"]
        rec1:C -> rec2
        rec2:CA -> "Value (of Field CA)" [minlen=2]
        rec3 [label="{<rec3>Record (sub-records-sub-record) | { <DA>Field DA | <DB>Field DB | <DN>... } }"]
        rec1:D -> "Records (sub-records)"
        "Records (sub-records)" -> rec3 [arrowhead=crow style=tapered penwidth=3]
        rec3:DA -> "Value (of Field DA)"
    }


data reference index paths
..........................

A `index path` is is a tuple of indexes/keys that is referencing one part or a value of a data structure.

The items of an index path are either of type int (specifying a list index in a :class:`Values` or
:class:`Records` instance) or of type str (specifying a field name of a :class:`Record` instance).

E.g. the index path for to reference in the above graph example the field **DA** from the record **Record (root)**
would be ``('D', 0, 'DA')``. The first item is referencing the field **D** in the root record. The second item **0** is
referencing the first item of the :class:`Records` instance/value of field **D**, which is a :class:`Record`
instance. And finally the last item **DA** specifies the field name in this :class:`Record` instance.

The hierarchically highest placed :class:`Record` instance in a data structure is called the `root record`,
and the :class:`Value` instances at the lowest level in a data structure are the leaves of a
data structure.

Each :class:`_Field` is providing apart from its field value also a reference to its root record
as well as a `root index`. The root index is an index path for to reference the :class:`_Field`
instance from the root record.

If the format/representation of the data value or of any references differs at one of the used systems
then a :class:`_Field` instance allows you to store a separate system-specific value.
For to access a system-specific value or reference in your data structure
you have to specify additionally to the index path also a `system identifier`
and optionally a `direction identifier`.


system and direction identifiers
--------------------------------

A `system id` is an user-defined string that is uniquely identifying a system and should consist of at least
two characters (see :data:`_ASP_SYS_MIN_LEN`).

A `direction id` is specifying the data flow direction. The two pre-defined direction ids are
:data:`FAD_FROM` for pulling data from a system or
:data:`FAD_ONTO` for pushing data onto a system.

The methods :meth:`~Record.pull` and :meth:`~Record.push` of the :class:`Record` class are used to pull/push
and convert system-specific data from/onto a system.
"""
import datetime
import keyword
from collections import OrderedDict
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Union, Generator, Type, cast

from ae.valid import correct_email, correct_phone       # type: ignore  # mypy --namespace-packages does not work


__version__ = '0.0.9'


ACTION_INSERT = 'INSERT'        #: insert action
ACTION_UPDATE = 'UPDATE'        #: update action
ACTION_UPSERT = 'UPSERT'        #: insert or update (if already exists) action
ACTION_DELETE = 'DELETE'        #: delete action
ACTION_SEARCH = 'SEARCH'        #: search action
ACTION_PARSE = 'PARSE'          #: parse action
ACTION_BUILD = 'BUILD'          #: build action
ACTION_PULL = 'PULL'            #: pull-from-system action
ACTION_PUSH = 'PUSH'            #: push-to-system action
ACTION_COMPARE = 'COMPARE'      #: compare action

# field aspect types/prefixes
FAT_IDX = 'idx'                 #: main/system field name within parent Record or list index within Records/Values
FAT_VAL = 'vle'                 #: main/system field value - storing one of the VALUE_TYPES instance
FAT_CLEAR_VAL = 'vwc'           #: field default/clear value (init by _Field.set_clear_val(), used by clear_leaves())
FAT_REC = 'rrd'                 #: root Record instance
FAT_RCX = 'rrx'                 #: field index path (idx_path) from the root Record instance
FAT_CAL = 'clc'                 #: calculator callable
FAT_CHK = 'chk'                 #: validator callable
FAT_CNV = 'cnv'                 #: system value converter callable
FAT_FLT = 'flt'                 #: field filter callable
FAT_SQE = 'sqc'                 #: SQL expression for to fetch field value from db

ALL_FATS = (FAT_IDX, FAT_VAL, FAT_CLEAR_VAL, FAT_REC, FAT_RCX, FAT_CAL, FAT_CHK, FAT_CNV, FAT_FLT, FAT_SQE)
""" tuple of all pre-defined field aspect types/prefixes """

FAD_FROM = 'From'               #: FROM field aspect direction
FAD_ONTO = 'Onto'               #: ONTO field aspect direction

IDX_PATH_SEP = '/'
""" separator character used for idx_path values (especially if field has a Record value).

don't use dot char because this is used e.g. for to separate system field names in xml element name paths.
"""

ALL_FIELDS = '**'
""" special key of fields_patches argument of Record.copy() for to allow aspect value patching for all fields. """

CALLABLE_SUFFIX = '()'          #: suffix for aspect keys - used by _Field.set_aspects()

_ASP_TYPE_LEN = 3               #: aspect key type string length
_ASP_DIR_LEN = 4                #: aspect key direction string length
_ASP_SYS_MIN_LEN = 2            #: aspect key system id string length


IDX_TYPES: Tuple[Type, ...] = (int, str)            #: tuple of classes/types used for system data index path items
# PATH_TYPES = IDX_TYPES + (tuple, )
PATH_TYPES = (int, str, tuple)                      #: path items, plus field name path, plus index path

AspectKeyType = str                                             #: type of a _Field aspect key
IdxItemType = Union[int, str]                                   #: types of idx_path items
IdxPathType = Tuple[IdxItemType, ...]                           #: idx_path type
IdxTypes = Union[IdxItemType, IdxPathType]                      #: types of either idx_path or idx_path items
NodeType = Union['Record', 'Records']                           #: node types (:data:`NODE_TYPES`)
ListType = Union['Values', 'Records']                           #: list/sequence types (:data:`LIST_TYPES`)
ValueType = Union['Value', 'Values', 'Record', 'Records']       #: value types (:data:`VALUE_TYPES`)
NodeChildType = Union['_Field', 'Record']                       #: node child types
FieldCallable = Callable[['_Field'], Any]                       #: callable with _Field argument
FieldValCallable = Callable[['_Field', Any], Any]               #: callable with _Field and additional argument


def aspect_key(type_or_key: str, system: AspectKeyType = '', direction: AspectKeyType = ''
               ) -> AspectKeyType:
    """ compiles an aspect key from the given args

    :param type_or_key:     either FAT_* type or full key (including already the system and direction)-
    :param system:          system id string (if type_or_key is a pure FAT_* constant).
    :param direction:       direction string FAD_* constant (if type_or_key is a pure FAT_* constant).
    :return:                compiled aspect key as string.
    """
    msg = f"aspect_key({type_or_key}, {system}, {direction}) error: "
    assert len(type_or_key) >= _ASP_TYPE_LEN, msg + "aspect type is too short"
    assert system == '' or len(system) >= _ASP_SYS_MIN_LEN, msg + "aspect system id is too short"
    assert direction == '' or len(direction) == _ASP_DIR_LEN, msg + "invalid aspect direction length"
    assert not type_or_key[0].islower() or type_or_key[:_ASP_TYPE_LEN] in ALL_FATS, msg + "invalid aspect type format"
    assert (system == '' or system[0].isupper()) and \
           (direction == '' or direction[0].isupper()), msg + "invalid system or direction format"

    key = type_or_key
    if len(key) == _ASP_TYPE_LEN:
        key += direction
    if len(key) <= _ASP_TYPE_LEN + _ASP_DIR_LEN:
        key += system

    assert key.isidentifier() and not keyword.iskeyword(key), msg + f"key '{key}' contains invalid characters"
    if type_or_key[:_ASP_TYPE_LEN] in ALL_FATS:
        assert key.count(FAD_FROM) <= 1 and key.count(FAD_ONTO) <= 1, msg + "direction duplicates"

    return key


def aspect_key_system(key: str) -> str:
    """ determines the system id string from an aspect key.

    :param key:     aspect key string.
    :return:        system id (SDI_* constant).
    """
    beg = _ASP_TYPE_LEN
    if len(key) > _ASP_TYPE_LEN + _ASP_DIR_LEN and key[beg:beg + _ASP_DIR_LEN] in (FAD_FROM, FAD_ONTO):
        beg += _ASP_DIR_LEN
    return key[beg:]


def aspect_key_direction(key: str) -> str:
    """ determines the direction id string from an aspect key.

    :param key:     aspect key string.
    :return:        direction id (FAD_* constant).
    """
    direction = key[_ASP_TYPE_LEN:_ASP_TYPE_LEN + _ASP_DIR_LEN]
    return direction if direction in (FAD_FROM, FAD_ONTO) else ''


def deeper(deepness: int, instance: Any) -> int:
    """ check and calculate resulting/remaining deepness for Record/_Field/Records.copy() when going one level deeper.

    :param deepness:    <0 will be returned unchanged until last level is reached (-1==full deep copy, -2==deep copy
                        until deepest Value, -3==deep copy until deepest _Field.
    :param instance:    instance to be processed/copied (if this method is returning != 0/zero).
    :return:            if deepness == 0 then return 0, if deepness < 0 then return 0 if the deepest level is reached,
                        else (deepness > 0) return deepness - 1.
    """
    if deepness > 0:
        remaining = deepness - 1
    elif deepness == -2 and isinstance(instance, Value) \
            or deepness == -3 and isinstance(instance, _Field) and isinstance(instance.value(), Value):
        remaining = 0
    else:
        remaining = deepness    # return unchanged if deepness in (0, -1) or == -2/-3 but not reached bottom/last level
    return remaining


def field_name_idx_path(field_name: Union[int, str, IdxPathType], return_root_fields: bool = False) -> IdxPathType:
    """ converts a field name path string into an index path tuple.

    :param field_name:          field name str or field name index/path string or field index tuple
                                or int (for Records index).
    :param return_root_fields:  pass True to also return len()==1-tuple for fields with no deeper path (def=False).
    :return:                    index path tuple (idx_path) or empty tuple if the field has no deeper path and
                                return_root_fields==False.
     """
    if isinstance(field_name, int):
        return cast(IdxPathType, (field_name, )) if return_root_fields else tuple()     # mypy - false positive w/o cast
    if isinstance(field_name, (tuple, list)):
        # mypy - false positive using () instead of tuple()
        return tuple(field_name) if return_root_fields or len(field_name) > 1 else tuple()  # mypy-"-

    idx_path: List[Union[int, str]] = list()
    nam_i = num_i = None
    last_i = len(field_name) - 2    # prevent splitting of 1- or 2-digit-indexed sys names, like e.g. NAME-1 or CD_ADD11
    for ch_i, ch_v in enumerate(field_name):
        if ch_v == IDX_PATH_SEP:
            if nam_i is not None:
                idx_path.append(field_name[nam_i:ch_i])
                nam_i = None
            elif num_i is not None:
                idx_path.append(int(field_name[num_i:ch_i]))
                num_i = None
            continue            # simply ignore leading, trailing and duplicate IDX_PATH_SEP chars

        if str.isdigit(ch_v) and ch_i < last_i:
            if num_i is None:
                num_i = ch_i
                if nam_i is not None:
                    idx_path.append(field_name[nam_i:num_i])
                    nam_i = None
        else:
            if nam_i is None:
                nam_i = ch_i
                if num_i is not None:
                    idx_path.append(int(field_name[num_i:nam_i]))
                    num_i = None

    if idx_path:
        if nam_i is not None:
            idx_path.append(field_name[nam_i:])
    elif return_root_fields:
        idx_path.append(field_name)

    return tuple(idx_path)


def field_names_idx_paths(field_names: Sequence[IdxPathType]) -> List[IdxPathType]:
    """ return list of the full idx paths names for all the fields specified in the field_names argument.

    :param field_names:     sequence/list/tuple of field (main or system) names.
    :return:                list of their idx paths names.
    """
    return [field_name_idx_path(field_name, return_root_fields=True) for field_name in field_names]


def idx_path_field_name(idx_path: IdxPathType, add_sep: bool = False) -> str:
    """ convert index path tuple/list into field name string.

    :param idx_path:    index path to convert.
    :param add_sep:     pass True to always separate index with IDX_PATH_SEP. False/Def will only put a separator char
                        if field value is a Record (for to separate the root field name from the sub field name).
    :return:            field name string.
    """
    assert isinstance(idx_path, (tuple, list)), f"idx_path_field_name() expects idx_path as tuple, got {type(idx_path)}"
    last_nam_idx = False
    field_name = ''
    for idx in idx_path:
        nam_idx = isinstance(idx, str)
        if field_name and (last_nam_idx and nam_idx or add_sep):
            field_name += IDX_PATH_SEP
        field_name += str(idx)
        last_nam_idx = nam_idx
    return field_name


def compose_current_index(node: Union[ListType, NodeType], idx_path: IdxPathType, use_curr_idx: List) -> IdxPathType:
    """ determine tuple with the current indexes.

    :param node:            root node/list (Record or Records/Values instance) to process.
    :param idx_path:        index path relative to root node passed in `node` arg.
    :param use_curr_idx:    list of index counters within `idx_path` where the current index has to be used.
    :return:                tuple of current indexes.
    """
    uci = use_curr_idx.copy()

    curr_idx: Tuple[Union[int, str], ...] = ()
    while True:
        idx, *idx2 = use_current_index(node, idx_path, uci, check_idx_type=True)
        curr_idx += (idx, )
        if not idx2:
            break
        if node.node_child((idx,)) is None:       # if idx not exists then assume sub-path idx2 is correct
            curr_idx += tuple(idx2)
            break

        n_v = node.value(idx, flex_sys_dir=True)        # mypy * 2
        assert isinstance(n_v, PARENT_TYPES), f"compose_current_index() expects {PARENT_TYPES} at {idx} of {node}"
        node = n_v
        idx_path = idx_path[1:]

    return curr_idx


def get_current_index(node: Union[ListType, NodeType]) -> Optional[IdxItemType]:
    """ get current index of passed `node`.

    :param node:    instance of Record or Records (real node) or Values (simple list).
    :return:        current index value.
    """
    return node.current_idx


def init_current_index(node: Union[ListType, NodeType], idx_path: IdxPathType, use_curr_idx: Optional[List]
                       ) -> IdxPathType:
    """ determine current index of `node` and if not set the initialize to the first index path item.

    :param node:            root node/list (Record or Records/Values instance) to process.
    :param idx_path:        index path relative to root node passed in `node` arg.
    :param use_curr_idx:    list of index counters within `idx_path` where the current index has to be used.
    :return:                tuple of current indexes.
    """

    idx, *idx2 = use_current_index(node, idx_path, use_curr_idx, check_idx_type=True)

    if node.current_idx is None:
        set_current_index(node, idx)

    return (idx, ) + tuple(idx2)


def set_current_index(node: Union[ListType, NodeType], idx: Optional[IdxItemType] = None,
                      add: Optional[int] = None) -> IdxItemType:
    """ set current index of `node`.

    :param node:            root node/list (Record or Records/Values instance) to process.
    :param idx:             index value to set (str for field name; int for list index); if given `add` will be ignored.
    :param add:             value to add to list index; will be ignored if `idx` arg get passed.
    :return:                the finally set/new index value.
    """
    msg = "set_current_index() expects "
    assert isinstance(node, PARENT_TYPES), msg + f"node arg of type {PARENT_TYPES}, but got {type(node)}"
    assert isinstance(idx, IDX_TYPES) ^ isinstance(add, int), msg + "either int/str in idx or int in add"

    if idx is None:
        # mypy * 2: false positive (already covered by last assert)
        assert isinstance(node.current_idx, int), msg + f"int type in index {node.current_idx!r}"
        assert isinstance(add, int), msg + f"int type in add argument: {add!r}"
        idx = node.current_idx + add

    assert isinstance(idx, (int, str)), msg + f"int/str type in idx argument: {idx!r}"      # mypy
    node.current_idx = idx

    if isinstance(node, LIST_TYPES):
        assert isinstance(idx, int), msg + f"int type for list types in idx argument ({idx!r})"         # mypy
        if node.idx_min is None or idx < node.idx_min:
            node.idx_min = idx
        if node.idx_max is None or idx > node.idx_max:
            node.idx_max = idx

    return idx


def use_current_index(node: Union[ListType, NodeType], idx_path: IdxPathType, use_curr_idx: Optional[List],
                      check_idx_type: bool = False, delta: int = 1) -> IdxPathType:
    """ determine index path of `node` by using current index of `node` if exists and is enabled by `use_curr_idx` arg.

    :param node:            root node/list (Record or Records/Values instance) to process.
    :param idx_path:        index path relative to root node passed in `node` arg.
    :param use_curr_idx:    list of index counters within `idx_path` where the current index has to be used.
    :param check_idx_type:  pass True to additionally check if the index type is correct (def=False).
    :param delta:           value for to decrease the list index counters within `use_curr_idx` (def=1).
    :return:                tuple of current indexes.
    """
    msg = "use_current_index() expects "
    assert isinstance(idx_path, (tuple, list)) and len(idx_path) > 0, msg + "non-empty idx_path"
    assert isinstance(use_curr_idx, (List, type(None))), msg + "None/List type for use_curr_idx"

    idx, *idx2 = idx_path

    idx_type: Union[Type[int], Type[str]]   # mypy
    if isinstance(node, LIST_TYPES):
        idx_type = int
    elif isinstance(node, Record):
        idx_type = str
    else:
        assert False, msg + f"value type of Values, Records or Record, but got {type(node)}"
    if check_idx_type:
        assert isinstance(idx, idx_type), f"index type {idx_type} in idx_path[0], but got {type(idx)}"

    if use_curr_idx:
        for level, val in enumerate(use_curr_idx):
            if val == 0 and node.current_idx is not None:
                idx = node.current_idx
            use_curr_idx[level] -= delta

    return (idx, ) + tuple(idx2)


def string_to_records(str_val: str, field_names: Sequence, rec_sep: str = ',', fld_sep: str = '=',
                      root_rec: 'Record' = None, root_idx: IdxPathType = ()) -> 'Records':
    """ convert formatted string into a :class:`Records` instance containing several :class:`Record` instances.

    :param str_val:     formatted string to convert.
    :param field_names: list/tuple of field names of each record
    :param rec_sep:     character(s) used in `str_val` for to separate the records.
    :param fld_sep:     character(s) used in `str_val` for to separate the field values of each record.
    :param root_rec:    root to which the returned records will be added.
    :param root_idx:    index path from root where the returned records will be added.
    :return:            converted :class:`Records` instance.
    """
    recs = Records()
    if str_val:
        for rec_idx, rec_str in enumerate(str_val.split(rec_sep)):
            fields = dict()
            for fld_idx, fld_val in enumerate(rec_str.split(fld_sep)):
                fields[field_names[fld_idx]] = fld_val
            recs.append(Record(fields=fields, root_rec=root_rec, root_idx=root_idx + (rec_idx,)))
            set_current_index(recs, idx=rec_idx)
    return recs


def template_idx_path(idx_path: IdxPathType, is_sub_rec: bool = False) -> bool:
    """ check/determine if `idx_path` is referring to template item.

    :param idx_path:    index path to check.
    :param is_sub_rec:  pass True to only check sub-record-fields (will then return always False for root-fields).
    :return:            True if `idx_path` is referencing a template item (with index zero/0), else False.
    """
    if len(idx_path) < 2:
        return not is_sub_rec
    for idx in idx_path:
        if isinstance(idx, int) and idx == 0:
            return True
    return False


def use_rec_default_root_rec_idx(rec: 'Record', root_rec: Optional['Record'], idx: Optional[IdxPathType] = (),
                                 root_idx: Optional[IdxPathType] = (), met: str = ""
                                 ) -> Tuple['Record', IdxPathType]:
    """ helper function for to determine resulting root record and root index.

    :param rec:         current :class:`Record` instance.
    :param root_rec:    default root record (def=`rec`).
    :param idx:         current index of `rec`.
    :param root_idx:    default root index.
    :param met:         calling method/function name (used only for assert error message, def='').
    :return:            resulting root record and root index (as tuple).
    """
    if root_rec is None:
        root_rec = rec
        if root_idx is not None:
            assert root_idx == (), met + ("(): " if met and not met.endswith(": ") else "") \
                                   + "root_idx has to be empty if no root_rec specified"
    if not root_idx:
        root_idx = () if idx is None else idx
    return root_rec, root_idx


def use_rec_default_sys_dir(rec: Optional['Record'], system: Optional[AspectKeyType], direction: Optional[AspectKeyType]
                            ) -> Tuple[str, str]:
    """ helper function for to determine resulting system/direction.

    :param rec:         current :class:`Record` instance.
    :param system:      default system id.
    :param direction:   default direction (see FAD_* constants).
    :return:            resulting system and direction (as tuple).
    """
    if rec is None:
        return "", ""
    if system is None:
        system = rec.system
    if direction is None:
        direction = rec.direction
    return system, direction


class Value(list):
    """ represents a value.

    This class inherits directly from the Python list class. Each instance can hold either a (single/atomic) value
    (which can be anything: numeric, char/string or any object) or a list of these single/atomic values.
    """
    def __getitem__(self, key: Union[slice, int]) -> Any:
        """ determine atomic value.

        :param key:     list index if value is a list.
        :return:        list item value.
        """
        try:
            return super().__getitem__(key)
        except IndexError:
            if not isinstance(key, int) or key not in (-1, 0):
                return None
            return ''

    def __setitem__(self, key: Union[slice, int], value: Any) -> None:
        """ set/initialize list item identified by `key` to the value passed in `value`.

        :param key:     list index if value is a list.
        :param value:   the new value of the list item.
        """
        while True:
            try:
                return super().__setitem__(key, value)
            except (IndexError, TypeError):
                if not isinstance(key, int):
                    raise IndexError(f"Value.__setitem__() expects key of type int, but got {key} of type {type(key)}")
                self.append(value)

    def __repr__(self) -> str:
        """ representation which can be used to serialize and re-create :class:`Value` instance.

        :return: Value representation string.
        """
        return "Value([" + ",".join(repr(v) for v in self) + "])"

    def __str__(self) -> str:
        """ string representation of this :class:`Value` instance.

        :return: Value string.
        """
        return "Value([" + ",".join(repr(v) for v in self) + "])"

    @property
    def initialized(self):
        """ flag if this :class:`Value` instance got already initialized.

        :return: True if already set to a value, else False.
        """
        return len(self)

    def node_child(self, idx_path: IdxPathType, moan: bool = False, **__) -> Optional['Value']:
        """ check if `idx_path` is correct (has to be empty) and if yes then return self.

        This method is for to simplify the data structure hierarchy implementation.

        :param idx_path:    this argument has to be an empty tuple/list.
        :param moan:        pass True for to raise AssertionError if `idx_path` is not empty.
        :return:            self or None (if `idx_path` is not empty and `moan` == False).
        """
        if len(idx_path) > 0:
            assert not moan, f"Value instance has no deeper node, but requesting {idx_path}"
            return None
        return self

    def value(self, *idx_path: IdxItemType, **__) -> Optional['Value']:
        """ check if `idx_path` is correct (has to be empty) and if yes then return self.

        This method is for to simplify the data structure hierarchy implementation.

        :param idx_path:    this argument has to be an empty tuple.
        :return:            self or None (if `idx_path` is not empty and `moan` == False).
        """
        assert isinstance(idx_path, (tuple, list)) and len(idx_path) == 0, \
            f"Value.value() expects empty idx_path list, but got {idx_path}"
        return self

    def val(self, *idx_path, **__):
        """ check if `idx_path` is correct (either empty or contain one int) and if yes then return list item.

        This method is for to simplify the data structure hierarchy implementation.

        :param idx_path:    this argument is either empty or contains a list index.
        :return:            atomic/single value or list item value or empty string.
        """
        idx_len = len(idx_path)
        if idx_len == 0 or (idx_len == 1 and isinstance(idx_path[0], int)):
            return self[idx_path[0] if idx_len else -1]
        return ''

    def set_val(self, val: Any, *idx_path: IdxItemType, **__):
        """ set a/the value of this instance.

        :param val:         simple/atomic value to be set.
        :param idx_path:    this argument is either empty or contains a list index.
        :return:            self.
        """
        assert isinstance(idx_path, (tuple, list)) and len(idx_path) <= 1, \
            f"Value.set_val({val}) idx_path list {idx_path} has more than one entry"
        assert not isinstance(val, VALUE_TYPES), f"Value.set_val({val}) got unexpected value type {type(val)}"
        self[cast(int, idx_path[0]) if isinstance(idx_path, (tuple, list)) and len(idx_path) > 0 else -1] = val
        return self

    def copy(self, *_, **__):
        """ copy the value of this Value instance into a new one.

        :return:                new Value instance containing the same immutable value.
        """
        return Value(super().copy())

    def clear_leaves(self, **__):
        """ clear/reset the value of this instance.

        use self[-1] = '' for to clear only the newest/top val.

        :return:    self.
        """
        self.clear()
        return self


class Values(list):
    """ ordered/mutable sequence/list, which contains 0..n instances of the class :class:`Value`.
    """
    def __init__(self, seq: Iterable = ()):
        """ create new :class:`Values` instance.

        :param seq:     Iterable used to initialize the new instance (pass list, tuple or other iterable).
        """
        super().__init__(seq)
        self.current_idx: Optional[int]       # mypy * 3
        self.idx_min: Optional[int]
        self.idx_max: Optional[int]
        self.current_idx = self.idx_min = self.idx_max = None

    def __repr__(self) -> str:
        return ("Records" if isinstance(self, Records) else "Values") + "([" + ",".join(repr(v) for v in self) + "])"

    def __str__(self) -> str:
        return ("Records" if isinstance(self, Records) else "Values") + "([" + ",".join(str(v) for v in self) + "])"

    def node_child(self, idx_path: IdxTypes, use_curr_idx: Optional[list] = None, moan: bool = False,
                   selected_sys_dir: Optional[dict] = None) -> Optional[ValueType]:
        """ determine and return node instance specified by `idx_path` if exists in this instance or underneath.

        :param idx_path:            index path to the node, relative to this instance.
        :param use_curr_idx:        list of counters for to specify if and which current indexes have to be used.
        :param moan:                flag for to check data integrity; pass True to raise AssertionError if not.
        :param selected_sys_dir:    optional dict for to return the currently selected system/direction.
        :return:                    found node instance or None if not found.
        """
        msg = f"node_child() of Values/Records instance {self} expects "
        if isinstance(idx_path, (tuple, list)):
            if len(idx_path) > 0 and not isinstance(idx_path[0], int):
                assert not moan, msg + f"int type in idx_path[0], got {type(idx_path)} in {idx_path}"
                return None
        elif not isinstance(idx_path, IDX_TYPES):
            assert not moan, msg + f"str or int type in idx_path, got {type(idx_path)} in {idx_path}"
            return None
        else:
            idx_path = field_name_idx_path(idx_path, return_root_fields=True)

        if not idx_path:
            assert not moan, msg + f"non-empty tuple or list or index string in idx_path {idx_path}"
            return None

        idx, *idx2 = use_current_index(self, idx_path, use_curr_idx)

        lst_len = len(self)
        if not isinstance(idx, int) or lst_len <= idx:
            assert not moan, f"Values/Records idx_path[0] {idx!r} is no int or is not less than list length {lst_len}"
            return None

        if len(idx_path) == 1:
            ret = super().__getitem__(idx)
            assert ret is not None or not moan, msg + f"valid key but got {idx} from idx_path {idx_path}"
            return ret

        return self[idx].node_child(idx2, use_curr_idx=use_curr_idx, moan=moan, selected_sys_dir=selected_sys_dir)

    def value(self, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = '', **kwargs
              ) -> Optional[ValueType]:
        """ determine the ValueType instance referenced by `idx_path` of this :class:`Values`/:class:`Records` instance.

        :param idx_path:    index path items.
        :param system:      system id.
        :param direction:   direction id.
        :param kwargs:      extra args (will be passed to underlying data structure).
        :return:            found Value or Values instance, or None if not found.
        """
        if len(idx_path) == 0:
            return self

        idx, *idx2 = idx_path
        assert isinstance(idx, int), f"{type(self)}.value expects int type in idx argument: {idx!r}"     # mypy
        return self[idx].value(*idx2, system=system, direction=direction, **kwargs)

    def set_value(self, value: ValueType, *idx_path: IdxItemType,
                  system: AspectKeyType = '', direction: AspectKeyType = '',
                  protect: bool = False, root_rec: Optional['Record'] = None, root_idx: IdxPathType = (),
                  use_curr_idx: list = None
                  ) -> Union['Values', 'Records']:
        """ set the ValueType instance referenced by `idx_path` of this :class:`Values`/:class:`Records` instance.

        :param value:           ValueType instance to set/change.
        :param idx_path:        index path items.
        :param system:          system id.
        :param direction:       direction id.
        :param protect:         pass True to prevent replacement of already existing `ValueType`.
        :param root_rec:        root record.
        :param root_idx:        root index.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this instance of :class:`Values` or :class:`Records`).
        """
        msg = f"{type(self)}.set_value() expects "
        assert len(idx_path) > 0, msg + "non-empty value in idx_path argument"

        if isinstance(self, Records):
            idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
            if root_idx:
                root_idx += (idx,)
            v_with_set_value = self[idx]                                # mypy
            assert isinstance(v_with_set_value, PARENT_TYPES), msg + f"{PARENT_TYPES} type in item {idx}"     # mypy
            v_with_set_value.set_value(value, *idx2, system=system, direction=direction, protect=protect,
                                       root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)
        else:
            idx = idx_path[0]
            assert isinstance(value, Value), msg + f" Value type in value argument, got {type(value)}"
            assert len(idx_path) == 1, msg + f"single index in idx_path argument, got {idx_path}"
            assert isinstance(idx, int), msg + f"int type in first item of idx_path, got {idx!r}"
            self[idx] = value
        return self

    def val(self, *idx_path: IdxItemType,
            system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
            use_curr_idx: list = None, **kwargs) -> Any:
        """ determine the user/system value referenced by `idx_path` of this :class:`Values`/:class:`Records` instance.

        :param idx_path:        index path items.
        :param system:          system id.
        :param direction:       direction id.
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param kwargs:          extra args (will be passed to underlying data structure).
        :return:                found user/system value, or None if not found or empty string if value was not set yet.
        """
        idx_len = len(idx_path)
        val: Any = None
        if idx_len == 0:
            val = list(self)
        else:
            idx, *idx2 = use_current_index(self, idx_path, use_curr_idx)
            if isinstance(idx, int) and idx < len(self):
                val = self[idx].val(*idx2, system=system, direction=direction, flex_sys_dir=flex_sys_dir,
                                    use_curr_idx=use_curr_idx, **kwargs)
        return val

    def set_val(self, val: Any, *idx_path: IdxItemType, protect: bool = False, extend: bool = True,
                use_curr_idx: list = None) -> 'Values':
        """ set the user/system value referenced by `idx_path` of this :class:`Values` instance.

        :param val:             user/system value to set/change.
        :param idx_path:        index path items.
        :param protect:         pass True to prevent replacement of already existing `ValueType`.
        :param extend:          pass True to allow extension of data structure.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this instance of :class:`Values`).
        """
        idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        assert isinstance(idx, int) and len(idx2) == 0, f"Values expects one int index, but got {idx_path}"
        value = val if isinstance(val, Value) else Value((val, ))
        list_len = len(self)
        if list_len <= idx:
            assert extend, "extend argument has to be True for to add Value instances to Values"
            for _ in range(idx - list_len):
                self.append(Value())
            self.append(value)
        else:
            assert not protect, "protect argument has to be True for to overwrite Value"
            self[idx] = value
        return self

    def copy(self, deepness: int = 0, root_rec: Optional['Record'] = None, root_idx: IdxPathType = (), **kwargs
             ) -> Union['Values', 'Records']:
        """ copy the values/records of this :class:`Values`/:class:`Records` instance.

        :param deepness:        deep copy levels: <0==see deeper(), 0==only copy current instance, >0==deep copy
                                to deepness value - _Field occupies two deepness: 1st=_Field, 2nd=Value).
        :param root_rec:        destination root record.
        :param root_idx:        destination index path (tuple of field names and/or list/Records indexes).
        :param kwargs:          additional arguments (will be passed on - most of them used by Record.copy).
        :return:                new instance of self (which is an instance of :class:`Values` or :class:`Records`).
        """
        ret = type(self)()      # create new instance of this list/class (Values or Records)
        for idx, rec in enumerate(self):
            if deeper(deepness, rec):
                rec = rec.copy(deepness=deeper(deepness, rec), root_rec=root_rec, root_idx=root_idx + (idx, ), **kwargs)
            ret.append(rec)
        return ret

    def clear_leaves(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                     reset_lists: bool = True
                     ) -> Union['Values', 'Records']:
        """ clear/reset the user/system values of all the leaves of this :class:`Values`/:class:`Records` instance.

        :param system:          system id.
        :param direction:       direction id (FAD_* constants).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param reset_lists:     pass False to prevent the reset of all the underlying lists.
        :return:
        """
        if reset_lists:
            self[1:] = []
        for rec in self:
            rec.clear_leaves(system=system, direction=direction, flex_sys_dir=flex_sys_dir, reset_lists=reset_lists)
        if len(self) > 0:
            self.current_idx = self.idx_min = 0
            self.idx_max = len(self) - 1
        else:
            self.current_idx = self.idx_min = self.idx_max = None
        return self


class Record(OrderedDict):
    """ instances of this mapping class are used to represent record-like data structures.

    isinstance(..., dict) not working if using MutableMapping instead of OrderedDict as super class. And dict
    cannot be used as super class because instance as kwarg will then not work: see the Groxx's answer in stackoverflow
    question at https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict/47361653#47361653.
    """
    def __init__(self, template: Optional['Records'] = None, fields: Optional[Iterable] = None,
                 system: AspectKeyType = '', direction: AspectKeyType = '', action: str = '',
                 root_rec: Optional['Record'] = None, root_idx: Optional[IdxPathType] = (),
                 field_items: bool = False):
        """ Create new Record instance, which is an ordered collection of _Field items.

        :param template:    pass Records instance to use first item/[0] as template (after deep copy / values cleared).
        :param fields:      OrderedDict/dict of _Field instances (field order is not preserved when using dict)
                            or Record instance (fields will be referenced, not copied!)
                            or list of (field_name, fld_or_val) tuples.
        :param system:      main/current system of this record,
        :param direction:   interface direction of this record.
        :param action:      current action (see ACTION_INSERT, ACTION_SEARCH, ACTION_DELETE, ...)
        :param root_rec:    root record of this record (def=self will be a root record).
        :param root_idx:    root index of this record (def=()).
        :param field_items: pass True to get Record items - using __getitem__() - as of type _Field (not as val()).
        """
        super().__init__()

        # using internal store of OrderedDict() while keeping code better readable/maintainable
        self._fields = self

        self.system: AspectKeyType = system
        self.direction: AspectKeyType = direction
        self.action: str = action
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx, met="Record.__init__")
        self.field_items: bool = field_items

        self.current_idx: Optional[str] = None

        if template and len(template) > 0:
            msg = "Record.__init__() expects "
            tpl_rec = template[0]
            assert isinstance(tpl_rec, Record), msg + f"Record type in first Records template item {tpl_rec}"  # mypy
            tpl_rec = tpl_rec.copy(deepness=-1, root_rec=root_rec, root_idx=root_idx)
            tpl_rec = tpl_rec.clear_leaves()
            for idx in tpl_rec.keys():
                field = tpl_rec.node_child((idx, ))
                assert isinstance(field, _Field), msg + f"_Field type in template Record, got {field}"    # mypy
                self._add_field(field)
        if fields:
            self.add_fields(fields, root_rec=root_rec, root_idx=root_idx)

        self.sys_name_field_map: Dict[str, _Field] = dict()  # map system field name as key to _Field instance(as value)
        self.collected_system_fields: List[_Field] = list()   # system fields found by collect_system_fields()

    def __repr__(self) -> str:
        ret = "Record("
        if self._fields:
            ret += "fields=" + ", ".join(repr(idx_path_field_name(k)) + ": " + repr(self._fields.val(*k))
                                         for k in self.leaf_indexes())
        return ret + ")"

    def __str__(self) -> str:
        return f"Record({', '.join(k for k in self.keys())})"

    # tried to make mypy happy with these overload declarations, but then flake8 is showing F811
    # @overload
    # def __contains__(self, idx_path: IdxTypes) -> bool: ...
    # @overload
    # def __contains__(self, idx_path: object) -> bool: ...

    def __contains__(self, idx_path: Union[IdxTypes, object]) -> bool:
        assert isinstance(idx_path, PATH_TYPES), f"Record.__contains__() expects {PATH_TYPES} in idx_path arg"   # mypy
        item = self.node_child(idx_path)
        # on executing self.pop() no __delitem__ will be called instead python OrderedDict first pops the item
        # then is calling this method, although super().__contains__() still returns True but then calls __getitem__()
        # (again with this instance where the item got already removed from). So next two lines are not helping:
        # if not item:
        #    item = super().__contains__(idx_path)
        # So finally had to over-ride the Record.pop() method.
        return bool(item)

    def __getitem__(self, key: IdxTypes) -> Any:
        ssd: Dict[str, str] = dict()
        child = self.node_child(key, moan=True, selected_sys_dir=ssd)
        # should actually not happen because with moan=True node_child() will raise AssertionError
        # if child is None:
        #    raise KeyError(f"There is no item with the key '{key}' in this Record/OrderedDict ({self})")
        return child if self.field_items or not isinstance(child, _Field) \
            else child.val(system=ssd.get('system', self.system), direction=ssd.get('direction', self.direction))

    def __setitem__(self, key: IdxTypes, value: Any):
        idx_path = field_name_idx_path(key, return_root_fields=True)
        self.set_node_child(value, *idx_path)

    def node_child(self, idx_path: IdxTypes, use_curr_idx: Optional[list] = None, moan: bool = False,
                   selected_sys_dir: Optional[dict] = None) -> Optional[Union[ValueType, NodeChildType]]:
        """ get the node child specified by `idx_path` relative to this :class:`Record` instance.

        :param idx_path:            index path or field name index string.
        :param use_curr_idx:        list of counters for to specify if and which current indexes have to be used.
        :param moan:                flag for to check data integrity; pass True to raise AssertionError if not.
        :param selected_sys_dir:    optional dict for to return the currently selected system/direction.
        :return:                    found node instance or None if not found.
        """
        msg = "Record.node_child() expects "
        if not isinstance(idx_path, (tuple, list)):
            if not isinstance(idx_path, str):
                assert not moan, msg + f"str type in idx_path[0], got {type(idx_path)} in {idx_path}"
                return None
            idx_path = field_name_idx_path(idx_path, return_root_fields=True)

        if not idx_path:
            assert not moan, msg + f"non-empty tuple or list in idx_path {idx_path}"
            return None

        idx, *idx2 = use_current_index(self, idx_path, use_curr_idx=use_curr_idx)
        if isinstance(idx, int):
            assert not moan, msg + f"str (not int) type in 1st idx_path {idx_path} item, got {type(idx_path)}"
            return None     # RETURN item not found (caller doing deep search with integer idx)

        # defensive programming: using self._fields.keys() although self._fields.items() gets item via get() in 3.5, for
        # .. to ensure _Field instances independent from self.field_items value (having py-tests for get() not items())
        for fld_nam, field in self._fields.items():
            if fld_nam == idx:
                if not idx2:
                    break
                fld = field.node_child(idx2, use_curr_idx=use_curr_idx, moan=moan, selected_sys_dir=selected_sys_dir)
                if fld is not None:
                    field = fld
                    break
            if not idx2 and field.has_name(idx, selected_sys_dir=selected_sys_dir):
                break
        else:
            assert not moan, msg + f"valid key but got {idx} from idx_path {idx_path}"
            field = None

        return field

    def set_node_child(self, fld_or_val: Any, *idx_path: IdxItemType,
                       system: AspectKeyType = None, direction: AspectKeyType = None,
                       protect: bool = False, root_rec: Optional['Record'] = None, root_idx: Optional[IdxPathType] = (),
                       use_curr_idx: Optional[list] = None, to_value_type: bool = False) -> 'Record':
        """ set/replace the child of the node specified by `idx_path` with the value of `fld_or_val`.

        :param fld_or_val:      field or value - for to be set.
        :param idx_path:        index path of the node child to set/replace.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param protect:         pass True to prevent the replacement of a node child.
        :param root_rec:        root record of this data structure.
        :param root_idx:        root index path of this node.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param to_value_type:   pass True ensure conversion of `fld_or_val` to a Value instance.
        :return:                self (this Record instance).
        """
        msg = "Record.set_node_child() expects "
        idx_len = len(idx_path)
        assert idx_len, msg + "2 or more args - missing field name/-path"
        assert isinstance(idx_path[0], str), \
            msg + f"string type in first item of Record idx_path {idx_path}, but got {type(idx_path[0])}"
        if idx_len == 1:
            nam_path = field_name_idx_path(idx_path[0])
            if nam_path:
                idx_path = tuple(nam_path)  # mypy - added tuple()
                idx_len = len(idx_path)

        system, direction = use_rec_default_sys_dir(self, system, direction)
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx,
                                                          met="Record.set_node_child")

        fld_idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        root_idx += (fld_idx, )
        if not isinstance(fld_or_val, NODE_CHILD_TYPES):
            use_current_index(self, idx_path, use_curr_idx, delta=-1)
            self.set_val(fld_or_val, *idx_path, system=system, direction=direction, protect=protect,
                         root_rec=root_rec, root_idx=root_idx[:-1], use_curr_idx=use_curr_idx,
                         to_value_type=to_value_type)

        elif fld_idx in self._fields:
            if idx_len == 1:
                assert not protect, msg + f"that the field {fld_idx} does not exist; pass protect=False to overwrite"
                super().__setitem__(fld_idx, fld_or_val)
                fld_or_val.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)

            else:
                ror = self.value(fld_idx, flex_sys_dir=True)    # if protect==True then should be of Record or Records
                if not isinstance(ror, NODE_TYPES):
                    assert not protect, msg + f"{NODE_TYPES} type in field value ({ror}[{idx_path}]), got {type(ror)}" \
                        f"; pass protect argument as False for to convert and overwrite"
                    ror = Record() if isinstance(idx2[0], str) else Records()
                    init_current_index(ror, tuple(idx2), use_curr_idx)
                    self.set_value(ror, fld_idx, root_rec=root_rec, root_idx=root_idx[:-1], use_curr_idx=use_curr_idx)
                ror.set_node_child(fld_or_val, *idx2, system=system, direction=direction, protect=protect,
                                   root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)

        elif idx_len == 1:
            assert isinstance(fld_or_val, _Field), msg + f"_Field type in {fld_or_val}"             # mypy
            assert isinstance(fld_idx, str), msg + f"str type in first index path item {fld_idx}"   # mypy
            self._add_field(fld_or_val, fld_idx)
            fld_or_val.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)

        else:
            use_current_index(self, idx_path, use_curr_idx, delta=-1)
            *rec_path, deep_fld_name = idx_path
            rec = self.node_child(tuple(rec_path), use_curr_idx=use_curr_idx)
            if not rec:     # if no deeper Record instance exists, then create new Record via empty dict and set_val()
                self.set_val(dict(), *rec_path, protect=protect, root_rec=root_rec, root_idx=root_idx[:-1],
                             use_curr_idx=use_curr_idx, to_value_type=to_value_type)
                rec = self.node_child(tuple(rec_path), use_curr_idx=use_curr_idx)
            use_current_index(self, idx_path, use_curr_idx, delta=len(rec_path))
            assert isinstance(rec, Record), msg + f"Record type in {rec_path} child {rec}"      # mypy
            rec.set_node_child(fld_or_val, deep_fld_name, system=system, direction=direction, protect=protect,
                               root_rec=root_rec, root_idx=idx_path[:-1], use_curr_idx=use_curr_idx)

        return self

    def value(self, *idx_path: IdxItemType, system: AspectKeyType = None, direction: AspectKeyType = None, **kwargs
              ) -> Optional[ValueType]:
        """ search the Value specified by `idx_path` and return it if found.

        :param idx_path:    index path of Value.
        :param system:      system id (pass None to use default system id of this `Record` instance).
        :param direction:   direction id (pass None to use default direction id of this `Record` instance).
        :param kwargs:      additional keyword args (to be passed onto underlying data structure).
        :return:            found Value instance of None if not found.
        """
        if len(idx_path) == 0:
            return self

        system, direction = use_rec_default_sys_dir(self, system, direction)
        idx, *idx2 = idx_path

        field = self.node_child((idx, ))
        if field:
            return field.value(*idx2, system=system, direction=direction, **kwargs)
        return None

    def set_value(self, value: ValueType, *idx_path: IdxItemType,
                  system: AspectKeyType = None, direction: AspectKeyType = None,
                  protect: bool = False, root_rec: Optional['Record'] = None, root_idx: IdxPathType = (),
                  use_curr_idx: Optional[list] = None) -> 'Record':
        """ set/replace the Value instance of the node specified by `idx_path`.

        :param value:           Value instance to be set/replaced.
        :param idx_path:        index path of the Value to be set.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param protect:         pass True to protect existing node value from to be changed/replaced.
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this Record instance).
        """
        system, direction = use_rec_default_sys_dir(self, system, direction)
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx, met="Record.set_value")
        idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        root_idx += (idx, )
        field = self.node_child((idx, ))
        assert isinstance(field, _Field), f"Record.set_value() expects _Field type in {idx} child {field}"    # mypy
        field.set_value(value, *idx2, system=system, direction=direction, protect=protect,
                        root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)
        return self

    def val(self, *idx_path: IdxItemType,
            system: AspectKeyType = None, direction: AspectKeyType = None, flex_sys_dir: bool = True,
            use_curr_idx: Optional[list] = None, **kwargs) -> Any:
        """ determine the user/system value referenced by `idx_path` of this :class:`Record` instance.

        :param idx_path:        index path items.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param kwargs:          extra args (will be passed to underlying data structure).
        :return:                found user/system value, or None if not found or empty string if value was not set yet.
        """
        system, direction = use_rec_default_sys_dir(self, system, direction)

        val: Any = None
        idx_len = len(idx_path)
        if idx_len == 0:
            val = OrderedDict()
            for idx, field in self._fields.items():
                val[idx] = field.val(system=system, direction=direction, flex_sys_dir=flex_sys_dir, **kwargs)
        else:
            idx, *idx2 = use_current_index(self, idx_path, use_curr_idx)
            if idx in self._fields:     # don't use _fields.keys() to also detect system field names
                # field = self._fields[idx]  ->  field = self._fields.get(idx)   # get() doesn't find sys fld names  ->
                ssd: Dict[str, str] = dict()
                field = self.node_child(idx, selected_sys_dir=ssd)
                val = field.val(*idx2, system=ssd.get('system', system), direction=ssd.get('direction', direction),
                                flex_sys_dir=flex_sys_dir, use_curr_idx=use_curr_idx, **kwargs)
        return val

    def set_val(self, val: Any, *idx_path: IdxItemType,
                system: Optional[AspectKeyType] = None, direction: Optional[AspectKeyType] = None,
                flex_sys_dir: bool = True, protect: bool = False, extend: bool = True,
                converter: Optional[FieldValCallable] = None,
                root_rec: Optional['Record'] = None, root_idx: Optional[IdxPathType] = (),
                use_curr_idx: Optional[list] = None, to_value_type: bool = False
                ) -> 'Record':
        """ set the user/system value referenced by `idx_path` of this :class:`Record` instance.

        :param val:             user/system value to be set/replaced.
        :param idx_path:        index path of the Value to be set.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param protect:         pass True to protect existing node value from to be changed/replaced.
        :param extend:          pass False to prevent extension of data structure.
        :param converter:       converter callable for to convert user values between systems.
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param to_value_type:   pass True ensure conversion of `val` to a Value instance.
        :return:                self (this Record instance).
        """
        if len(idx_path) == 0:
            return self.add_fields(val)         # RETURN

        sys_s: AspectKeyType    # mypy
        dir_s: AspectKeyType
        sys_s, dir_s = use_rec_default_sys_dir(self, system, direction)
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx, met="Record.set_val")

        idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        root_idx += (idx, )
        field: _Field
        if idx in self._fields:
            ssd: Dict[str, str] = dict()
            field = cast(_Field, self.node_child(idx, selected_sys_dir=ssd))    # mypy
            sys_s, dir_s = ssd.get('system', sys_s), ssd.get('direction', dir_s)
        else:
            assert extend, "Record.set_val() expects extend=True for to add new fields"
            field = _Field(root_rec=root_rec or self, root_idx=root_idx)
            assert isinstance(idx, str), f"Record.set_val() expects str type in first item of {idx_path}"     # mypy
            self._add_field(field, idx)
            protect = False

        field.set_val(val, *idx2, system=sys_s, direction=dir_s, flex_sys_dir=flex_sys_dir,
                      protect=protect, extend=extend, converter=converter,
                      root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx, to_value_type=to_value_type)
        return self

    def _add_field(self, field: '_Field', idx: str = '') -> 'Record':
        """ add _Field instance to this Record instance.

        :param field:   _Field instance to add.
        :param idx:     name/key/idx string for to map and identify this field (mostly identical to field.name()).
        :return:        self.
        """
        msg = f"_add_field({field}, {idx}): "
        assert isinstance(field, _Field), msg + f"field arg has to be of type _Field (not {type(field)})"
        assert isinstance(idx, str), msg + f"idx arg has to be of type str (not {type(idx)})"

        if idx:
            field.set_name(idx)
        else:
            idx = field.name()

        assert idx not in self._fields, msg + f"Record '{self}' has already a field with the name '{idx}'"

        super().__setitem__(idx, field)     # self._fields[idx] = field
        return self

    def add_fields(self, fields: Iterable, root_rec: 'Record' = None, root_idx: IdxPathType = ()) -> 'Record':
        """ adding fields to this Record instance.

        :param fields:      either a dict, a Record or a list with (key/field_name, val/_Field) tuples.
                            Key strings that are containing digits/numbers are interpreted as name/idx paths (then also
                            the specified sub-Records/-Fields will be created).
                            Values can be either _Field instances or field values.
        :param root_rec:    root record of this record (def=self will be a root record).
        :param root_idx:    root index of this record (def=()).
        :return:            self
        """
        if isinstance(fields, dict):
            items: Iterable = fields.items()
        else:
            items = fields
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx, met="Record.add_fields")

        for name, fld_or_val in items:
            idx_path = field_name_idx_path(name, return_root_fields=True)
            if not root_idx and isinstance(fld_or_val, _Field):
                root_idx = fld_or_val.root_idx()

            self.set_node_child(fld_or_val, *idx_path, protect=True, root_rec=root_rec, root_idx=root_idx)
        return self

    def add_system_fields(self, system_fields: Iterable[Iterable[Any]], sys_fld_indexes: Dict = None,
                          system: AspectKeyType = None, direction: AspectKeyType = None, extend: bool = True
                          ) -> 'Record':
        """ add/set fields to this :class:`Record` instance from the field definition passed into `system_fields`.

        Make sure before you call this method that this :class:`Record` instance has the system and direction
        attributes specified/set.

        :param system_fields:   tuple/list of tuples/lists with system and main field names and optional field aspects.
                                The index of the field names and aspects within the inner tuples/lists get specified
                                by sys_fld_indexes.
        :param sys_fld_indexes: mapping/map-item-indexes of the inner tuples of system_fields. Keys are field aspect
                                types (FAT_* constants), optionally extended with a direction (FAD_* constant) and a
                                system (SDI_* constant). If the value aspect key (FAT_VAL) contains a callable then
                                it will be set as the calculator (FAT_CAL) aspect; if contains a field value then also
                                the clear_val of this field will be set to the specified value.
        :param system:          system of the fields to be added - if not passed self.system will be used.
        :param direction:       direction (FAD constants) of the fields to be added - if not passed used self.direction.
        :param extend:          True=add not existing fields, False=apply new system aspects only on existing fields.
        :return:                self
        """
        msg = "add_system_fields() expects "
        assert isinstance(system_fields, (tuple, list)) and len(system_fields) > 0, \
            msg + f"non-empty list or tuple in system_fields arg, got {system_fields}"
        system, direction = use_rec_default_sys_dir(self, system, direction)
        assert system and direction, msg + "non-empty system/direction values (either from args or self)"
        sys_nam_key = aspect_key(FAT_IDX, system=system, direction=direction)
        if sys_fld_indexes is None:
            sys_fld_indexes = {sys_nam_key: 0,
                               FAT_IDX: 1,
                               FAT_VAL: 2,
                               FAT_FLT + FAD_ONTO: 3,
                               FAT_CNV + FAD_FROM: 4,
                               FAT_CNV + FAD_ONTO: 5}
        else:
            assert isinstance(sys_fld_indexes, dict), msg + f"sys_fld_indexes arg as dict, got {type(sys_fld_indexes)}"
            if sys_nam_key not in sys_fld_indexes:  # check if sys name key is specified without self.system
                sys_nam_key = aspect_key(FAT_IDX, direction=direction)
            assert FAT_IDX in sys_fld_indexes and sys_nam_key in sys_fld_indexes, \
                msg + f"field and system field name aspects in sys_fld_indexes arg {sys_fld_indexes}"
        err = [_ for _ in system_fields if sys_nam_key not in sys_fld_indexes or sys_fld_indexes[sys_nam_key] >= len(_)]
        assert not err, msg + f"system field name/{sys_nam_key} in each system_fields item; missing in {err}"

        for fas in system_fields:
            map_len = len(fas)
            sfi = sys_fld_indexes.copy()    # fresh copy needed because field names and converter get popped from sfi

            fld_nam_i = sfi.pop(FAT_IDX)
            if map_len <= fld_nam_i or fas[fld_nam_i] is None:
                continue
            field_name = fas[fld_nam_i]
            if isinstance(field_name, (tuple, list)):
                idx_path = tuple(field_name)
                field_name = field_name[-1]
            else:
                idx_path = field_name_idx_path(field_name, return_root_fields=True)
                field_name = idx_path[-1]

            sys_name = fas[sfi.pop(sys_nam_key)].strip('/')     # strip needed for Sihot elem names only

            records = self.value(idx_path[0], system='', direction='')
            if template_idx_path(idx_path, is_sub_rec=True) and records:
                # if template sub-record then also add sys name/converter/calculator/filter/... to each sub Record
                idx_paths = [(idx_path[0], idx, ) + idx_path[2:] for idx in range(len(records))]
            else:
                idx_paths = [idx_path, ]
            for path_idx, idx_path in enumerate(idx_paths):
                field = self.node_child(idx_path)
                field_created = not bool(field)
                if not field:
                    if not extend:
                        continue
                    field = _Field(root_rec=self, root_idx=idx_path)
                    field.set_name(field_name)
                assert isinstance(field, _Field), msg + f"_Field type in {idx_path} child, got {type(field)}"    # mypy

                # add additional aspects: first always add converter and value (for to create separate system value)
                cnv_func = None
                cnv_key = FAT_CNV + direction
                if map_len > sfi.get(cnv_key, map_len):
                    cnv_func = fas[sfi.pop(cnv_key)]
                elif map_len > sfi.get(FAT_CNV, map_len):
                    cnv_func = fas[sfi.pop(FAT_CNV)]
                if cnv_func:
                    field.set_converter(cnv_func, system=system, direction=direction, protect=False,
                                        root_rec=self, root_idx=idx_path)
                # now add all other field aspects (allowing calculator function specified in FAT_VAL aspect)
                for f_asp, a_idx in sfi.items():
                    if f_asp.startswith(FAT_CNV):
                        continue                    # skip converter for other direction
                    if map_len > a_idx and fas[a_idx] is not None \
                            and f_asp[_ASP_TYPE_LEN:] in ('', direction, system, direction + system):
                        if not f_asp.startswith(FAT_VAL):
                            field.set_aspect(fas[a_idx], f_asp, system=system, direction=direction, protect=True)
                        elif callable(fas[a_idx]):     # is a calculator specified in value/FAT_VAL item
                            field.set_calculator(fas[a_idx], system=system, direction=direction, protect=True)
                        else:                       # init field and clear val
                            val = fas[a_idx]
                            if path_idx == 0:
                                field.set_val(val, system=system, direction=direction, protect=True,
                                              root_rec=self, root_idx=idx_path)
                            field.set_clear_val(val, system=system, direction=direction)

                self.set_node_child(field, *idx_path, protect=field_created, root_rec=self, root_idx=())
                # set sys field name and root_idx (after set_node_child() which is resetting sys root_idx to field name)
                # multiple sys names for the same field - only use the first one (for parsing but allow for building)
                if not field.name(system=system, direction=direction, flex_sys_dir=False):
                    field.set_name(sys_name, system=system, direction=direction, protect=True)

                if sys_name not in self.sys_name_field_map:
                    self.sys_name_field_map[sys_name] = field   # on sub-Records only put first row's field

        return self

    def collect_system_fields(self, sys_fld_name_path: Sequence, path_sep: str) -> List['_Field']:
        """ compile list of system :class:`_Field` instances of this :class:`Record` instance.

        :param sys_fld_name_path:   sequence/tuple/list of system field names/keys.
        :param path_sep:            system field name/key separator character(s).
        :return:                    list of :class:'_Field` instances which are having system field name/keys set.
        """
        self.collected_system_fields = list()

        deep_sys_fld_name = sys_fld_name_path[-1]
        full_path = path_sep.join(sys_fld_name_path)
        for sys_name, field in self.sys_name_field_map.items():
            if sys_name == deep_sys_fld_name or sys_name == full_path or full_path.endswith(path_sep + sys_name):
                if field not in self.collected_system_fields:
                    self.collected_system_fields.append(field)

        return self.collected_system_fields

    def compare_leaves(self, rec: 'Record', field_names: Iterable = (), exclude_fields: Iterable = ()) -> List[str]:
        """ compare the leaf 'compare' values of this :class:`Record` instance with the one passed into `rec`.

        'Compare values' are simplified user/system values generated by :meth:`Record.compare_val`.

        :param rec:             other :class:`Record` instance to compare to.
        :param field_names:     field names to include in compare; pass empty tuple (==default) to include all fields.
        :param exclude_fields:  field names to exclude from compare.
        :return:                list of str with the differences between self and `rec`.
        """
        def _excluded():
            return (field_names and idx_path[0] not in field_names and idx_path[-1] not in field_names) \
                                or (idx_path[0] in exclude_fields or idx_path[-1] in exclude_fields)
        dif = list()
        found_idx = list()
        for idx_path in self.leaf_indexes(system='', direction=''):
            if _excluded():
                continue
            found_idx.append(idx_path)
            this_val = self.compare_val(*idx_path)
            if idx_path in rec:
                that_val = rec.compare_val(*idx_path)
                if this_val != that_val:
                    dif.append(f"Different val in {idx_path}: {self.system}:{this_val!r} != {rec.system}:{that_val!r}")
            elif this_val:  # silently skip/ignore fields with empty value in this record if field doesn't exist in rec
                dif.append(f"Field {self.system}:{idx_path}={self.val(*idx_path)} does not exist in the other Record")

        for idx_path in rec.leaf_indexes(system='', direction=''):
            if _excluded():
                continue
            if idx_path not in found_idx:
                dif.append(f"Field {rec.system}:{idx_path}={rec.val(*idx_path)} does not exist in this Record")

        return dif

    def compare_val(self, *idx_path: IdxItemType) -> Any:
        """ determine normalized/simplified user/system value of the node specified by `idx_path`.

        :param idx_path:    index path to the node.
        :return:            normalized/simplified compare value.
        """
        field = self.node_child(idx_path)
        assert isinstance(field, _Field), \
            f"Record.compare_val() expects _Field type at {idx_path}, got {type(field)}"    # mypy
        idx = field.name()
        val = self.val(*idx_path, system='', direction='')

        if isinstance(val, str):
            if idx == 'SfId':
                val = val[:15]
            elif 'name' in idx.lower():
                val = val.capitalize()
            elif 'Email' in idx:
                val, _ = correct_email(val.lower())
            elif 'Phone' in idx:
                val, _ = correct_phone(val)
            val = val.strip()
            if len(val) > 39:
                val = val[:39].strip()
            if val == '':
                val = None
        elif isinstance(val, (datetime.date, datetime.datetime)):
            val = val.toordinal()

        return val

    def copy(self, deepness: int = 0, root_rec: Optional['Record'] = None, root_idx: IdxPathType = (),
             onto_rec: Optional['Record'] = None, filter_fields: Optional[FieldCallable] = None,
             fields_patches: Optional[Dict[str, Dict[str, Union[str, ValueType, FieldCallable]]]] = None) -> 'Record':
        """ copy the fields of this record.

        :param deepness:        deep copy level: <0==see deeper(), 0==only copy this record instance, >0==deep copy
                                to deepness value - _Field occupies two deepness: 1st=_Field, 2nd=Value).
        :param root_rec:        destination root record - using onto_rec/new record if not specified.
        :param root_idx:        destination root index (tuple/list with index path items: field names, list indexes).
        :param onto_rec:        destination record; pass None to create new Record instance.
        :param filter_fields:   method called for each copied field (return True to filter/hide/not-include into copy).
        :param fields_patches:  dict[field_name_or_ALL_FIELDS:dict[aspect_key:val_or_callable]] for to set/overwrite
                                aspect values in each copied _Field instance). The keys of the outer dict are either
                                field names or the ALL_FIELDS value; aspect keys ending with the CALLABLE_SUFFIX
                                have a callable in the dict item that will be called for each field with the field
                                instance as argument; the return value of the callable will then be used as the (new)
                                aspect value.
                                Set the aspect value that stores the field value (aspect key == :data:`FAT_VAL`)
                                by passing a data structure instance (of type :data:`ValueType`).
        :return:                new/extended record instance.
        """
        msg = "Record.copy() expects "
        new_rec = onto_rec is None
        if new_rec:
            onto_rec = Record()
        if root_rec is None:
            root_rec = onto_rec
        assert onto_rec is not self, msg + "different Record instance; cannot copy to self (same Record instance)"
        assert isinstance(onto_rec, Record), msg + f"destination of type Record, got {type(onto_rec)}"  # mypy

        for idx, field in self._fields.items():
            if filter_fields:
                assert callable(filter_fields)
                if filter_fields(field):
                    continue

            if deeper(deepness, field):
                field = field.copy(deepness=deeper(deepness, field), onto_rec=None if new_rec else onto_rec,
                                   root_rec=root_rec, root_idx=root_idx + (idx, ),
                                   filter_fields=filter_fields, fields_patches=fields_patches)
            elif idx in onto_rec:
                field = onto_rec.node_child((idx, ))

            if fields_patches:
                if ALL_FIELDS in fields_patches:
                    field.set_aspects(allow_values=True, **fields_patches[ALL_FIELDS])
                if idx in fields_patches:
                    field.set_aspects(allow_values=True, **fields_patches[idx])
                idx = field.name()      # update field name and root rec ref and idx if changed by field_patches
                field.set_system_root_rec_idx(root_rec=root_rec, root_idx=root_idx + (idx, ))

            if new_rec:
                onto_rec._add_field(field, idx)
            else:
                onto_rec.set_node_child(field, idx)

        return onto_rec

    def clear_leaves(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                     reset_lists: bool = True
                     ) -> 'Record':
        """ clear the leaf values including this :class:`Record` instance and all deeper data structures.

        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param reset_lists:     pass False to prevent reset of sub-lists.
        :return:
        """
        for field in self._fields.values():
            field.clear_leaves(system=system, direction=direction, flex_sys_dir=flex_sys_dir, reset_lists=reset_lists)
        return self

    def leaves(self, system: AspectKeyType = None, direction: AspectKeyType = None, flex_sys_dir: bool = True
               ) -> Generator['_Field', None, None]:
        """ generate leaves/_Field-instances of this :class:`Record` instance.

        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        system, direction = use_rec_default_sys_dir(self, system, direction)
        for field in self._fields.values():
            yield from field.leaves(system=system, direction=direction, flex_sys_dir=flex_sys_dir)

    def leaf_indexes(self, *idx_path: IdxItemType, system: AspectKeyType = None, direction: AspectKeyType = None,
                     flex_sys_dir: bool = True) -> Generator[IdxPathType, None, None]:
        """ generate leaf-/_Field-index paths for all fields of this :class:`Record` instance.

        :param idx_path:        index path to be added as base index path (index path to this `Record` instance).
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        system, direction = use_rec_default_sys_dir(self, system, direction)
        for idx, field in self._fields.items():
            fld_idx = idx_path + (idx, )
            yield from field.leaf_indexes(*fld_idx, system=system, direction=direction, flex_sys_dir=flex_sys_dir)

    def leaf_names(self, system: AspectKeyType = '', direction: AspectKeyType = '',
                   col_names: Iterable = (), field_names: Iterable = (),
                   exclude_fields: Iterable = (), name_type: Optional[str] = None) -> Tuple[IdxTypes, ...]:
        """ compile a tuple of name types (specified by `name_type`) for this :class:`Record` instance.

        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param col_names:       system field/column names to include; pass empty tuple (==default) to include all.
        :param field_names:     field names to include; pass empty tuple (==default) to include all fields.
        :param exclude_fields:  field names to exclude.
        :param name_type:       type of name to be included/returned - see available name types underneath.
        :return:                tuple of field names/indexes of the included/found leaves.

        Possible values for the `name_type` argument are:

        * 's': user/system field/column name.
        * 'f': field name.
        * 'r': root name (index path converted into string by :func:`idx_path_field_name`).
        * 'S': index path with user/system field/column name of leaf.
        * 'F': index path tuple.
        *  None: names depends on each leaf:
            * root name if leaf is not a root field.
            * user/system name if `system` is not empty/None.
            * field name.
        """
        names = list()
        ret_name: IdxTypes
        for field in self.leaves(system=system, direction=direction, flex_sys_dir=False):
            idx_path = field.root_idx(system=system, direction=direction)
            if not template_idx_path(idx_path):
                continue
            sys_name = field.name(system=system or self.system, direction=direction or self.direction,
                                  flex_sys_dir=False)
            if not sys_name or (col_names and sys_name not in col_names):
                continue
            fld_name = field.name()
            root_name = idx_path_field_name(idx_path)
            if not (field_names and fld_name not in field_names and root_name not in field_names
                    or fld_name in exclude_fields or root_name in exclude_fields):
                if name_type == 's':
                    ret_name = sys_name
                elif name_type == 'f':
                    ret_name = fld_name
                elif name_type == 'r':
                    ret_name = root_name
                elif name_type == 'S':
                    ret_name = tuple(idx_path[:-1]) + (sys_name, )
                elif name_type == 'F':
                    ret_name = idx_path
                else:
                    ret_name = root_name if len(idx_path) > 1 and idx_path[0] == fld_name \
                        else (sys_name if system else fld_name)
                if ret_name:
                    names.append(ret_name)

        return tuple(names)

    def merge_leaves(self, rec: 'Record',
                     system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                     extend: bool = True) -> 'Record':
        """ merge the leaves of the other record in `rec` into this :class:`Record` instance.

        :param rec:             other `Record` to merge into this one.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param extend:          pass False to prevent extension of this data structure.
        :return:                self (this :class:`Record` instance).
        """
        msg = "Record.merge_leaves() expects "
        for idx_path in rec.leaf_indexes(system=system, direction=direction, flex_sys_dir=flex_sys_dir):
            dst_field = self.node_child(idx_path)
            if extend or dst_field:
                src_field = rec.node_child(idx_path)
                assert isinstance(src_field, _Field), msg + f"_Field type at {idx_path}, got {type(src_field)}"   # mypy
                if dst_field:
                    assert isinstance(dst_field, _Field), msg + f"_Field type at {idx_path}: {type(dst_field)}"   # mypy
                    # noinspection PyProtectedMember
                    dst_field.set_aspects(allow_values=True, **src_field._aspects)
                elif extend:
                    self.set_node_child(src_field, *idx_path, system='', direction='')
        return self

    def match_key(self, match_fields: Iterable) -> tuple:
        """ make tuple of user/system values for all the fields in `match_fields`.

        :param match_fields:    Iterable with field names/index paths.
        :return:                tuple of user/system values.
        """
        return tuple([self.val(fn) for fn in match_fields])

    def merge_values(self, rec: 'Record',
                     system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                     extend: bool = True) -> 'Record':
        """ merge user/system values of the other record in `rec` into this :class:`Record` instance.

        :param rec:             other `Record` to merge into this one.
        :param system:          system id (pass None to use default system id of this `Record` instance).
        :param direction:       direction id (pass None to use default direction id of this `Record` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param extend:          pass False to prevent extension of this data structure.
        :return:                self (this :class:`Record` instance).
        """
        for idx_path in rec.leaf_indexes(system=system, direction=direction, flex_sys_dir=flex_sys_dir):
            if not extend and idx_path[0] not in self._fields:
                continue
            val = rec.val(*idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
            if val is not None:
                self.set_val(val, *idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        return self

    def missing_fields(self, required_fields: Iterable = ()) -> List[Tuple[IdxItemType, ...]]:
        """ check field-names/index-paths specified in `required_fields`.

        :param required_fields:     list/tuple/iterable of field names or index paths of required fields.
        :return:                    list of index paths for the ones that are missing or having an empty/None value.
        """
        missing = list()
        for alt in required_fields:
            if not isinstance(alt, tuple):
                alt = (alt, )
            for idx in alt:
                if self.val(idx, system='', direction=''):
                    break
            else:
                missing.append(alt)
        return missing

    def pop(self, idx: str, default: Optional['_Field'] = None) -> Optional['_Field']:  # type: ignore
        """ check if field name exists and if yes then remove the :class:`_Field` instance from this `Record` instance.

        :param idx:     field name.
        :param default: return value if a field with the name specified by idx does not exist in this Record.
        :return:        removed :class:`_Field` instance if found, else None.

        This method got added because the OrderedDict.pop() method does not call __delitem__() (see also __contains__())
        """
        field = self._fields.get(idx)
        # assert isinstance(field, _Field), f"Record.pop() expects _Field type at {idx}, got {type(field)}"    # mypy
        if field:
            super().__delitem__(idx)
        elif default is not None:
            field = default
        return field

    def pull(self, from_system: AspectKeyType) -> 'Record':
        """ pull all user/system values and convert them into field values.

        :param from_system:     system id of the system to pull from.
        :return:                self.
        """
        msg = "Record.pull() expects "
        assert from_system, msg + "non-empty value in from_system argument"
        for idx_path in self.leaf_indexes(system=from_system, direction=FAD_FROM):    # _fields.values():
            if len(idx_path) >= 3 and isinstance(idx_path[1], int):
                value = self.value(idx_path[0], system=from_system, direction=FAD_FROM, flex_sys_dir=True)
                assert isinstance(value, PARENT_TYPES), msg + f"{PARENT_TYPES} type of value at {idx_path[0]}"    # mypy
                set_current_index(value, idx=idx_path[1])
            field = self.node_child(idx_path)
            assert isinstance(field, _Field), msg + f"_Field type at {idx_path}, got {type(field)}"       # mypy
            field.pull(from_system, self, idx_path)
        return self

    def push(self, onto_system: AspectKeyType) -> 'Record':
        """ push field values of this :class:`Record` instance to the related user/system values (converted).

        :param onto_system:     system id of the system to push to.
        :return:                self.
        """
        msg = "Record.push() expects "
        assert onto_system, msg + "non-empty value in onto_system argument"
        for idx_path in self.leaf_indexes(system=onto_system, direction=FAD_ONTO):
            field = self.node_child(idx_path)
            assert isinstance(field, _Field), msg + f"_Field type at {idx_path}, got {type(field)}"       # mypy
            field.push(onto_system, self, idx_path)
        return self

    def set_current_system_index(self, sys_fld_name_prefix: str, path_sep: str, idx_val: Optional[int] = None,
                                 idx_add: Optional[int] = 1) -> Optional['Record']:
        """ check and if possible set the current system index of this :class:`Record` instance.

        :param sys_fld_name_prefix: user/system field name prefix.
        :param path_sep:            user/system name path separator.
        :param idx_val:             new current system index value to set (if passed then `idx_add` will be ignored).
        :param idx_add:             increment current system index value with the passed int value.
        :return:                    self (this `Record` instance) if current index got changed, else None.
        """
        msg = "Record.set_current_system_index() expects "
        prefix = sys_fld_name_prefix + path_sep
        for sys_path, field in self.sys_name_field_map.items():
            if sys_path.startswith(prefix):
                rec = field.root_rec(system=self.system, direction=self.direction)
                assert isinstance(rec, Record), msg + f"Record instance as root record, got {type(rec)}"  # mypy
                idx_path = field.root_idx(system=self.system, direction=self.direction)
                for off, idx in enumerate(idx_path):
                    if isinstance(idx, int):
                        value = rec.value(*idx_path[:off], flex_sys_dir=True)
                        assert isinstance(value, PARENT_TYPES), msg + f"{PARENT_TYPES} type at {idx_path[:off]}"  # mypy
                        set_current_index(value, idx=idx_val, add=idx_add)
                        return self
        return None

    def set_env(self, system: AspectKeyType = None, direction: AspectKeyType = None, action: str = None,
                root_rec: Optional['Record'] = None, root_idx: Optional[IdxPathType] = ()) -> 'Record':
        """ set the environment (system/direction/action) of this :class:`Record` instance.

        :param system:          system id (pass None to leave unchanged).
        :param direction:       direction id (pass None to leave unchanged).
        :param action:          action id (pass None to leave unchanged).
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :return:                self.
        """
        if system is not None:
            self.system = system
        if direction is not None:
            self.direction = direction
        if action is not None:
            self.action = action
        root_rec, root_idx = use_rec_default_root_rec_idx(self, root_rec, root_idx=root_idx, met="Record.set_env")

        # for idx in self._fields.keys():
        #    field = self._fields.get(idx)
        #    field.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx + (idx,))
        for idx_path in self.leaf_indexes(system=system, direction=direction):
            field = self.node_child(idx_path)
            assert isinstance(field, _Field), f"Record.set_env() expects _Field type at {idx_path}"       # mypy
            field.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx + idx_path)

        return self

    def sql_columns(self, from_system: AspectKeyType, col_names: Iterable = ()) -> List[str]:
        """ return list of sql column names for given system.

        :param from_system: system from which the data will be selected/fetched.
        :param col_names:   optionally restrict to select columns to names given in this list.
        :return:            list of sql column names.
        """
        column_names = list()
        for field in self._fields.values():
            if len(field.root_idx(system=from_system, direction=FAD_FROM)) == 1:
                name = field.aspect_value(FAT_IDX, system=from_system, direction=FAD_FROM)
                if name and (not col_names or name in col_names):
                    column_names.append(name)
        return column_names

    def sql_select(self, from_system: AspectKeyType, col_names: Iterable = ()) -> List[str]:
        """ return list of sql column names/expressions for given system.

        :param from_system: system from which the data will be selected/fetched.
        :param col_names:   optionally restrict to select columns to names given in this list.
        :return:            list of sql column names/expressions.
        """
        column_expressions = list()
        for field in self._fields.values():
            if len(field.root_idx(system=from_system, direction=FAD_FROM)) == 1:
                name = field.aspect_value(FAT_IDX, system=from_system, direction=FAD_FROM)
                if name and (not col_names or name in col_names):
                    expr = field.aspect_value(FAT_SQE, system=from_system, direction=FAD_FROM) or ""
                    if expr:
                        expr += " AS "
                    column_expressions.append(expr + name)
        return column_expressions

    def to_dict(self, filter_fields: Optional[FieldCallable] = None,
                key_type: Union[Type[str], Type[tuple], None] = str,
                push_onto: bool = True,
                use_system_key: bool = True, put_system_val: bool = True, put_empty_val: bool = False,
                system: AspectKeyType = None, direction: AspectKeyType = None) -> Dict[IdxTypes, Any]:
        """ copy Record leaf values into a dict.

        :param filter_fields:   callable returning True for each field that need to be excluded in returned dict, pass
                                None to include all fields (if put_empty_val == True).
        :param key_type:        type of dict keys: None=field name, tuple=index path tuple, str=index path string (def).
        :param push_onto:       pass False to prevent self.push(system).
        :param use_system_key:  pass False to put leaf field name/index; def=True for to use system field name/keys,
                                specified by the system/direction args.
        :param put_system_val:  pass False to include/use main field val; def=True for to include system val specified
                                by the system/direction args.
        :param put_empty_val:   pass True to also include fields with an empty value (None/'').
        :param system:          system id for to determine included leaf and field val (if put_system_val == True).
        :param direction:       direction id for to determine included leaf and field val (if put_system_val == True).
        :return:                dict of filtered leaf user/system values with field names/idx_path-tuples as their key.
        """
        msg = "Record.to_dict() expects "
        assert key_type is None or key_type is tuple or key_type is str, \
            msg + "None, tuple or str in key_type argument"
        system, direction = use_rec_default_sys_dir(self, system, direction)
        if push_onto and system:
            self.push(system)

        ret: Dict[IdxTypes, Any] = dict()
        for idx_path in self.leaf_indexes(system=system, direction=direction):
            field = self.node_child(idx_path)
            assert isinstance(field, _Field), msg + f"_Field type at {idx_path}, got {type(field)}"  # mypy
            key: IdxTypes = field.name(system=system, direction=direction, flex_sys_dir=False)
            if key and (not filter_fields or not filter_fields(field)):
                key_path = tuple(idx_path[:-1] + (key,)) if system and use_system_key else idx_path
                if key_type == tuple:
                    key = key_path
                elif key_type == str:
                    key = idx_path_field_name(key_path)
                if put_system_val:
                    val = self.val(*idx_path, system=system, direction=direction)
                else:
                    val = self.val(*idx_path, system='', direction='')
                if put_empty_val or val not in (None, ''):
                    ret[key] = val
        return ret

    def update(self, mapping=(), **kwargs):
        """ update this `Record` instance - overwriting/extending OrderedDict/super().update() for to return self.

        :param mapping:     mapping to use for to update this :class:`Record` instance.
        :param kwargs:      optional keyword arguments.
        :return:            self (this :class:`Record` instance).
        """
        super().update(mapping, **kwargs)
        return self     # implemented only for to get self as return value


class Records(Values):
    """ Records class.

    Each instance of this :class:`Records` class is a list of 0..n :class:`Record` instances.

    The not overwritten methods of the inherited :class:`Values` class are also available - like e.g.
    :meth:`Values.node_child` or :meth:`Values.val`.
    """
    def __init__(self, seq: Iterable = ()):
        """ create new :class:`Records` instance.

        :param seq:     Iterable used to initialize the new instance (pass list, tuple or other iterable).
        """
        super().__init__(seq)
        self.match_index: Dict[Tuple, List[Record]] = dict()

    def __getitem__(self, key: Union[slice, IdxTypes]) -> Union[ValueType, List[ValueType]]:    # type: ignore
        if isinstance(key, slice):
            return super().__getitem__(key)     # slice results in list type return
        child = self.node_child(key, moan=True)
        # if child is None:
        #    raise KeyError(f"There is no item with the idx_path '{key}' in this Records instance ({self})")
        assert child is not None   # mypy: actually not needed because node_child(..moan=True) will raise AssertionError
        return child

    def __setitem__(self, key: Union[IdxTypes, slice], value: Any):
        if isinstance(key, slice):
            super().__setitem__(key, value)
        else:
            idx_path = field_name_idx_path(key, return_root_fields=True)
            self.set_node_child(value, *idx_path)

    def set_node_child(self, rec_or_fld_or_val, *idx_path: IdxItemType,
                       system: AspectKeyType = '', direction: AspectKeyType = '',
                       protect: bool = False,
                       root_rec: Optional[Record] = None, root_idx: Optional[IdxPathType] = (),
                       use_curr_idx: Optional[list] = None) -> 'Records':
        """ set/replace the child of the node specified by `idx_path` with the value of `rec_or_fld_or_val`.

        :param rec_or_fld_or_val: record, field or value - for to be set.
        :param idx_path:        index path of the node child to set/replace.
        :param system:          system id (pass None to use default system id of this `Records` instance).
        :param direction:       direction id (pass None to use default direction id of this `Records` instance).
        :param protect:         pass True to prevent the replacement of a node child.
        :param root_rec:        root record of this data structure.
        :param root_idx:        root index path of this node.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this `Records` instance).
        """
        idx_len = len(idx_path)
        assert idx_len, f"Records.set_node_child() idx_path {idx_path} too short; expected one or more items"

        idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        assert isinstance(idx, int), \
            f"Records.set_node_child() 1st item of idx_path {idx_path} has to be integer, got {type(idx)}"

        for _ in range(idx - len(self) + 1):
            self.append(Record(template=self, root_rec=root_rec, root_idx=root_idx))
            protect = False

        if root_idx:
            root_idx += (idx, )
        if idx_len == 1:
            assert not protect, "protect has to be False to overwrite Record"
            if not isinstance(rec_or_fld_or_val, Record):
                rec_or_fld_or_val = Record(template=self, fields=rec_or_fld_or_val,
                                           system='' if root_idx else system, direction='' if root_idx else direction,
                                           root_rec=root_rec, root_idx=root_idx)
            super().__setitem__(idx, rec_or_fld_or_val)
        else:
            rec = cast(Record, self[idx])
            rec.set_node_child(rec_or_fld_or_val, *idx2, system=system, direction=direction, protect=protect,
                               root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)
        return self

    def set_val(self, val: Any, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = '',
                flex_sys_dir: bool = True, protect: bool = False, extend: bool = True,
                converter: Optional[FieldValCallable] = None,
                root_rec: Optional['Record'] = None, root_idx: Optional[IdxPathType] = (),
                use_curr_idx: Optional[list] = None) -> 'Records':
        """ set the user/system value referenced by `idx_path` of this :class:`Records` instance.

        :param val:             user/system value to be set/replaced.
        :param idx_path:        index path of the Value to be set.
        :param system:          system id (pass None to use default system id of this `Records` instance).
        :param direction:       direction id (pass None to use default direction id of this `Records` instance).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param protect:         pass True to protect existing node value from to be changed/replaced.
        :param extend:          pass False to prevent extension of data structure.
        :param converter:       converter callable for to convert user values between systems.
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Records instance.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this Records instance).
        """
        if len(idx_path) == 0:
            for i_x, row in enumerate(val):
                self.set_node_child(row, i_x, system=system, direction=direction,
                                    protect=protect, root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)
            return self                                 # RETURN

        idx, *idx2 = init_current_index(self, idx_path, use_curr_idx)
        assert isinstance(idx, int), f"Records expects first index of type int, but got {idx}"

        list_len = len(self)
        if root_idx:
            root_idx += (idx, )
        if list_len <= idx:
            assert extend, "extend has to be True for to add Value instances to Values"
            for _ in range(idx - list_len + 1):
                self.append(Record(template=self, root_rec=root_rec, root_idx=root_idx))
                protect = False

        if not idx2:
            assert not protect, f"Records.set_val() pass protect=False to overwrite {idx}"
            # noinspection PyTypeChecker
            # without above: strange PyCharm type hint warning: Type 'int' doesn't have expected attribute '__len__'
            self[idx] = val if isinstance(val, Record) else Record(template=self, fields=val,
                                                                   root_rec=root_rec, root_idx=root_idx)

        else:
            rec = self[idx]
            assert isinstance(rec, Record), f"Records can only contain Record instances, got {type(rec)}"
            rec.set_val(val, *idx2, system=system, direction=direction, flex_sys_dir=flex_sys_dir,
                        protect=protect, extend=extend, converter=converter, root_rec=root_rec, root_idx=root_idx,
                        use_curr_idx=use_curr_idx)

        return self

    def append_record(self, root_rec: Record, root_idx: IdxPathType = (), from_rec: Optional[Record] = None,
                      clear_leaves: bool = True) -> Record:
        """ add/append Record to this :class:`Records` instance.

        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Records instance.
        :param from_rec:        :class:`Record` instance to append, if not passed then use a copy of the first/template
                                Record of this :class:`Records` instance, else create new :class:`Record` instance.
        :param clear_leaves:    pass False to not clear the leaf values.
        :return:                added/appended :class:`Record` instance.
        """
        assert isinstance(root_rec, Record), "Records.append_record() expects Record instance in the root_rec arg"
        recs_len = len(self)
        tpl_rec = (cast(Record, self[0]) if recs_len else Record(root_rec=root_rec, root_idx=root_idx)) \
            if from_rec is None else from_rec

        new_rec = tpl_rec.copy(deepness=-1, root_rec=root_rec, root_idx=root_idx + (recs_len,))
        self.append(new_rec)

        if clear_leaves:
            new_rec.clear_leaves()      # clear fields and set init/default values

        return new_rec

    def compare_records(self, records: 'Records', match_fields: Iterable,
                        field_names: Iterable = (), exclude_fields: Iterable = (),
                        record_comparator: Optional[Callable[[Record, Record], List[str]]] = None) -> List[str]:
        """ compare the records of this instance with the ones passed in the `records` argument.

        :param records:         other instance of :class:`Records` to be compared against self.
        :param match_fields:    iterable with field names/index paths for to determine each `Record` id/pkey.
        :param field_names:     iterable with field names/index paths that get compared.
        :param exclude_fields:  iterable with field names/index-paths that get excluded from to be compared.
        :param record_comparator: optional callable for additional compare (called for each Record).
        :return:                list of differences.
        """
        records.index_match_fields(match_fields)
        processed_match_keys = list()

        dif: List[str] = list()
        for idx, rec in enumerate(self):
            match_key = rec.match_key(match_fields)
            if match_key in records.match_index:
                for p_rec in records.match_index[match_key]:
                    dif.extend(rec.compare_leaves(p_rec, field_names=field_names, exclude_fields=exclude_fields))
                    if callable(record_comparator):
                        dif.extend(record_comparator(rec, p_rec))
                processed_match_keys.append(match_key)
            else:
                dif.append(f"Record {idx} of this Records instance not found via {match_key}; rec={rec}")

        for match_key, p_recs in records.match_index.items():
            if match_key in processed_match_keys:
                continue
            for p_rec in p_recs:
                dif.append(f"Pulled Record not found in this Records instance via {match_key}; rec={p_rec}")

        return dif

    def index_match_fields(self, match_fields: Iterable) -> 'Records':
        """ create/initialize match index for this :class:`Records` instance (stored in `match_index` attribute).

        :param match_fields:    iterable with field names/index paths for to determine each `Record` id/pkey.
        :return:                self (this :class:`Records` instance).
        """
        for rec in self:
            match_key = rec.match_key(match_fields)
            if match_key in self.match_index:
                self.match_index[match_key].append(rec)
            else:
                self.match_index[match_key] = [rec]
        return self

    def leaves(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True
               ) -> Generator['_Field', None, None]:
        """ generate leaves/_Field-instances of this :class:`Records` instance.

        :param system:          system id (pass None to use default system id of the underlying `Record` instances).
        :param direction:       direction id (pass None to use default direction of the underlying `Record` instances).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        for rec in self:
            yield from rec.leaves(system=system, direction=direction, flex_sys_dir=flex_sys_dir)

    def leaf_indexes(self, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = '',
                     flex_sys_dir: bool = True) -> Generator[IdxPathType, None, None]:
        """ generate leaf-/_Field-index paths for all fields of this :class:`Records` instance.

        :param idx_path:        index path to be added as base index path (index path to this `Records` instance).
        :param system:          system id (pass None to use default system id of the underlying `Record` instances).
        :param direction:       direction id (pass None to use default direction of the underlying `Record` instances).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        for idx, rec in enumerate(self):
            item_idx = idx_path + (idx, )
            yield from rec.leaf_indexes(*item_idx, system=system, direction=direction, flex_sys_dir=flex_sys_dir)

    def merge_records(self, records: 'Records', match_fields: Iterable = ()) -> 'Records':
        """ merge the records passed in `records` into this :class:`Records` instance.

        :param records:         records to be merged in.
        :param match_fields:    match fields used to identify already existing records (merge values in this cases).
        :return:                self.
        """
        if len(self) == 0 or not match_fields:
            self.extend(records)
        else:
            if not self.match_index:
                self.index_match_fields(match_fields)
            for rec in records:
                match_key = rec.match_key(match_fields)
                if match_key in self.match_index:
                    for this_rec in self.match_index[match_key]:
                        this_rec.update(rec)
                else:
                    self.append(rec)
        return self

    def set_env(self, system: Optional[AspectKeyType] = '', direction: Optional[AspectKeyType] = '',
                root_rec: Optional[Record] = None, root_idx: Optional[IdxPathType] = ()) -> 'Records':
        """ set the environment (system/direction/action) of each record underneath this :class:`Records` instance.

        :param system:          system id (pass None to leave unchanged).
        :param direction:       direction id (pass None to leave unchanged).
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :return:                self.
        """
        for idx, rec in enumerate(self):
            rec.set_env(system=system, direction=direction, root_rec=root_rec,
                        # only extend with Records/list index if there is a Record above this Records instance
                        root_idx=root_idx + (idx, ) if root_idx else ())
        return self


class _Field:
    """ Internal/Private class used by :class:`Record` for to create record field instances.

    An instance of :class:`_Field` is representing one record field. The field properties are internally stored
    within a private dict (:data:`_Field._aspects`) and are called the 'aspects' of a field.

    Field aspects get used by a field instance e.g. for to:
    * store field value(s)
    * define callable(s) for to convert, filter or validate field values
    * associate the root record and root index
    * store any other user-defined field properties (like SQL column expressions, comments, ...)

    The :data:`FAT_ALL` constant contains all pre-defined aspects (see the other FAT_* constants defined at the
    top of this module). These values are called 'aspect keys' and are used as dict keys in the private dict.

    Each aspect can additionally have a separate property for each systems/directions - in this case the aspect
    key gets extended with direction/system ids. The two available direction ids are pre-defined by the constants
    :data:`FAD_FROM` and :data:`FAD_ONTO`. The system ids are not defined in this module, they have to be defined
    by the application. Aspect keys can be compiled with the function :func:`aspect_key`.
    """
    def __init__(self, root_rec: Optional[Record] = None, root_idx: IdxPathType = (), allow_values: bool = False,
                 **aspects):
        self._aspects: Dict[str, Any] = dict()
        self.add_aspects(allow_values=allow_values, **aspects)
        if root_rec is not None:
            self.set_root_rec(root_rec)
        if root_idx:
            self.set_root_idx(root_idx)

        assert FAT_REC in self._aspects, "_Field need to have a root Record instance"
        assert FAT_RCX in self._aspects, "_Field need to have an index path from the root Record instance"

        if FAT_VAL not in self._aspects and FAT_CAL not in self._aspects:
            self._aspects[FAT_VAL] = Value()
        if FAT_IDX not in self._aspects:
            idx = self.root_idx()
            assert len(idx) > 0
            self._aspects[FAT_IDX] = idx[0]

    def __repr__(self):
        names = self.name()
        values = repr(self.val())
        sys_dir_names = list()
        for idx_key, name in self._aspects.items():
            if idx_key.startswith(FAT_IDX) and len(idx_key) > _ASP_TYPE_LEN:
                sys_dir_names.append((idx_key, name))
        for idx_key, name in sys_dir_names:
            val_key = self.aspect_exists(FAT_VAL,
                                         system=aspect_key_system(idx_key), direction=aspect_key_direction(idx_key))
            if val_key and len(val_key) > _ASP_TYPE_LEN:
                values += "|" + f"{name}={self._aspects.get(val_key)}"
            else:
                names += "|" + name

        return f"{names}=={values}"

    def __str__(self):
        # return "_Field(" + repr(self._aspects) + ")"
        return "_Field(" + ", ".join([str(k) + ": " + str(v)
                                      for k, v in self._aspects.items() if not k.startswith(FAT_REC)]) + ")"

    def __getitem__(self, key):
        child = self.node_child(key, moan=True)
        # child is None should actually not happen because with moan=True node_child() will raise AssertionError
        # if child is None:
        #    raise KeyError(f"There is no item with the idx_path '{key}' in this _Field ({self})")
        return child

    def node_child(self, idx_path: IdxTypes, use_curr_idx: Optional[list] = None, moan: bool = False,
                   selected_sys_dir: Optional[dict] = None) -> Optional[Union[ValueType, NodeChildType]]:
        """ get the node child specified by `idx_path` relative to this :class:`_Field` instance.

        :param idx_path:            index path or field name index string.
        :param use_curr_idx:        list of counters for to specify if and which current indexes have to be used.
        :param moan:                flag for to check data integrity; pass True to raise AssertionError if not.
        :param selected_sys_dir:    optional dict for to return the currently selected system/direction.
        :return:                    found node instance or None if not found.
        """
        msg = f"node_child() of _Field {self} expects "
        if isinstance(idx_path, (tuple, list)):
            if len(idx_path) > 0 and not isinstance(idx_path[0], IDX_TYPES):
                assert not moan, msg + f"str or int in idx_path[0], got {type(idx_path[0])} ({idx_path[0]})"
                return None
        elif not isinstance(idx_path, IDX_TYPES):
            assert not moan, msg + f"str or int type in idx_path, but got {type(idx_path)} (idx={idx_path})"
            return None
        else:
            idx_path = field_name_idx_path(idx_path, return_root_fields=True)

        if not idx_path:
            assert not moan, msg + f"non-empty tuple or list or index string in idx_path {idx_path}"
            return None

        value = self.aspect_value(FAT_VAL)
        if not isinstance(value, VALUE_TYPES):
            assert not moan, msg + f"value type of {VALUE_TYPES} but got {type(value)}"
            return None

        return value.node_child(idx_path, use_curr_idx=use_curr_idx, moan=moan, selected_sys_dir=selected_sys_dir)

    def value(self, *idx_path: IdxItemType,
              system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = False
              ) -> Optional[ValueType]:
        """ search the Value specified by `idx_path` and return it if found.

        :param idx_path:        index path of Value.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass True to allow fallback to main (non-user/-system) value.
        :return:                found Value instance of None if not found.
        """
        value = None
        val_or_cal = self.aspect_value(FAT_VAL, FAT_CAL, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        if val_or_cal is not None:
            if callable(val_or_cal):
                value = val_or_cal(self)
                if value is not None and not isinstance(value, VALUE_TYPES):
                    value = Value((value, ))
            else:
                value = val_or_cal
        assert not flex_sys_dir and value is None or isinstance(value, VALUE_TYPES), \
            f"_Field.value({idx_path}, {system}, {direction}, {flex_sys_dir}): value '{val_or_cal}'/'{value}'" \
            f" has to be of type {VALUE_TYPES}"
        if value and len(idx_path) > 0:
            value = value.value(*idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        return value

    def set_value(self, value: ValueType, *idx_path: IdxItemType,
                  system: AspectKeyType = '', direction: AspectKeyType = '',
                  protect: bool = False, root_rec: 'Record' = None, root_idx: IdxPathType = (),
                  use_curr_idx: Optional[list] = None) -> '_Field':
        """ set/replace the Value instance of the node specified by `idx_path`.

        :param value:           Value instance to be set/replaced.
        :param idx_path:        index path of the Value to be set.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param protect:         pass True to protect existing node value from to be changed/replaced.
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                self (this _Field instance).
        """
        msg = f"_Field.set_value({value}, {idx_path}, {system}, {direction}, {protect}): "
        assert isinstance(value, VALUE_TYPES), msg + f"expects value types {VALUE_TYPES}, got {type(value)}"

        if isinstance(value, NODE_TYPES) and not idx_path and (system != '' or direction != ''):
            fld_sys = fld_dir = ''
        else:
            fld_sys, fld_dir = system, direction

        r_rec = self.root_rec(system=fld_sys, direction=fld_dir)
        assert isinstance(r_rec, Record), msg + f"expects Record type for root rec, got {type(r_rec)}"    # mypy
        root_rec, root_idx = use_rec_default_root_rec_idx(r_rec, root_rec,
                                                          idx=self.root_idx(system=fld_sys, direction=fld_dir),
                                                          root_idx=root_idx,
                                                          met=msg)
        assert root_rec is not None and root_idx, msg + f"root Record {root_rec} or index {root_idx} missing"

        key = aspect_key(FAT_VAL, system=fld_sys, direction=fld_dir)

        if not idx_path:
            assert not protect or key not in self._aspects, \
                msg + f"value key {key} already exists as aspect ({self._aspects[key]})"
            self._aspects[key] = value
            self.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)
        else:
            self._aspects[key].set_value(value, *idx_path, system=system, direction=direction, protect=protect,
                                         root_rec=root_rec, root_idx=root_idx, use_curr_idx=use_curr_idx)

        return self

    def val(self, *idx_path: IdxItemType,
            system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
            use_curr_idx: Optional[list] = None, **kwargs) -> Any:
        """ determine the user/system value referenced by `idx_path`.

        :param idx_path:        index path items.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param kwargs:          extra args (will be passed to underlying data structure).
        :return:                found user/system value, or None if not found or empty string if value was not set yet.
        """
        value = self.value(system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        # mypy - assert below is actually not needed because value of self should never be None
        assert value is not None
        return value.val(*idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir,
                         use_curr_idx=use_curr_idx, **kwargs)

    def set_val(self, val: Any, *idx_path: IdxItemType,
                system: AspectKeyType = '', direction: AspectKeyType = '',
                flex_sys_dir: bool = True, protect: bool = False, extend: bool = True,
                converter: Optional[FieldValCallable] = None,
                root_rec: Optional['Record'] = None, root_idx: IdxPathType = (),
                use_curr_idx: Optional[list] = None, to_value_type: bool = False) -> '_Field':
        """ set the user/system value referenced by `idx_path`.

        :param val:             user/system value to be set/replaced.
        :param idx_path:        index path of the Value to be set.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param protect:         pass True to protect existing node value from to be changed/replaced.
        :param extend:          pass False to prevent extension of data structure.
        :param converter:       converter callable for to convert user values between systems.
        :param root_rec:        root Record instance of this data structure.
        :param root_idx:        root index to this node/Record instance.
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :param to_value_type:   pass True ensure conversion of `val` to a Value instance.
        :return:                self (this _Field instance).
        """
        idx_len = len(idx_path)
        value = self.aspect_value(FAT_VAL, system=system, direction=direction,
                                  flex_sys_dir=flex_sys_dir or bool(idx_len))

        if idx_len == 0:
            if converter:   # create system value if converter is specified and on leaf idx_path item
                self.set_converter(converter, system=system, direction=direction, protect=not extend,
                                   root_rec=root_rec, root_idx=root_idx)
                value = self.aspect_value(FAT_VAL, system=system, direction=direction, flex_sys_dir=flex_sys_dir)

            val_is_value = isinstance(val, VALUE_TYPES)
            if val_is_value \
                    or isinstance(val, (list, dict)) and to_value_type \
                    or value is None \
                    or not isinstance(value, Value):
                assert extend and not protect, \
                    f"_Field.set_val({val}): value {value} exists - pass extend={extend}/protect={protect}"
                value = val if val_is_value \
                    else (Record() if isinstance(val, dict)
                          else ((Records() if isinstance(val[0], dict) else Values()) if isinstance(val, list)
                                else Value())
                          )
                self.set_value(value, system=system, direction=direction,
                               protect=protect, root_rec=root_rec, root_idx=root_idx)
            self.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)

            if val_is_value:
                return self             # RETURN

        elif isinstance(value, (Value, type(None))):
            assert extend and not protect, \
                f"_Field.set_val({val}, {idx_path}): value {value} exists - change extend={extend}/protect={protect}"
            value = Record() if isinstance(idx_path[0], str) \
                else (Records() if idx_len > 1 or isinstance(val, dict) else Values())
            init_current_index(value, idx_path, use_curr_idx)
            self.set_value(value, protect=protect, root_rec=root_rec, root_idx=root_idx)

        value.set_val(val, *idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir,
                      protect=protect, extend=extend, converter=converter, root_rec=root_rec, root_idx=root_idx,
                      use_curr_idx=use_curr_idx)
        return self

    def leaf_value(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = False
                   ) -> Optional[ValueType]:
        """ determine the leaf value of this field (and optionally system/direction).

        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                the main or user/system value of this leaf/field or None if deeper value
                                exists and `flex_sys_dir` is False.

        Used also for to check if a deeper located sys field exists in the current data structure.
        """
        value = self.value(system=system, direction=direction, flex_sys_dir=True)
        if not flex_sys_dir and not isinstance(value, NODE_TYPES) \
                and not self.aspect_value(FAT_IDX, system=system, direction=direction, flex_sys_dir=flex_sys_dir):
            value = None
        return value

    def leaves(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True
               ) -> Generator['_Field', None, None]:
        """ generate all sub-leaves/_Field-instances underneath this :class:`_Field` instance.

        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        value = self.leaf_value(system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        if isinstance(value, NODE_TYPES):
            yield from value.leaves(system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        elif value is not None:
            yield self

    def leaf_indexes(self, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = '',
                     flex_sys_dir: bool = True) -> Generator[IdxPathType, None, None]:
        """ generate leaf-/_Field-index paths for all sub-fields underneath (if exist) or this :class:`_Field` instance.

        :param idx_path:        index path to this `_Field` instance.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                leaf/_Field-instance generator.
        """
        value = self.leaf_value(system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        if isinstance(value, NODE_TYPES):
            yield from value.leaf_indexes(*idx_path, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        elif value is not None:
            yield idx_path

    def find_aspect_key(self, *aspect_types: AspectKeyType,
                        system: Optional[AspectKeyType] = '', direction: Optional[AspectKeyType] = ''
                        ) -> Optional[AspectKeyType]:
        """ search for the passed `aspect_types` in this :class:`_Field` instance.

        :param aspect_types:    aspect types (dict key prefixes) to search for.
        :param system:          system id ('' stands for the main/system-independent value).
        :param direction:       direction id ('' stands for the main/system-independent value).
        :return:                the full aspect key of the first found aspect that is matching the
                                passed aspect type and optionally also the passed system and direction ids.

        The search will done in the following order:
        * all passed aspect types including the passed system/direction ids.
        * all passed aspect types including the passed system and both directions (if direction id get not passed).
        * all passed aspect types including the passed system and without direction id.
        * all passed aspect types without system and direction ids.
        """
        keys = list()
        if direction and system:
            for aspect_type in aspect_types:
                keys.append(aspect_key(aspect_type, system=system, direction=direction))
        else:
            assert not direction, \
                f"_Field.find_aspect_key({aspect_types}, {system}, {direction}) direction without system not allowed"
            if system:
                for aspect_type in aspect_types:
                    for chk_dir in (FAD_ONTO, FAD_FROM):
                        keys.append(aspect_key(aspect_type, system=system, direction=chk_dir))
        if system:
            for aspect_type in aspect_types:
                keys.append(aspect_key(aspect_type, system=system))
        for aspect_type in aspect_types:
            keys.append(aspect_key(aspect_type))

        for key in keys:
            if key in self._aspects:
                return key

        return None

    def set_env(self, system: Optional[AspectKeyType] = '', direction: Optional[AspectKeyType] = '',
                root_rec: Optional[Record] = None, root_idx: Optional[IdxPathType] = ()) -> '_Field':
        """ set the environment (system/direction/action) of each record underneath this :class:`_Field` instance.

        :param system:          system id (don't pass or pass None to leave unchanged).
        :param direction:       direction id (don't pass or pass None to leave unchanged).
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                self (this :class:`_Field` instance).
        """
        # we cannot use self.value() for calculator fields because the rec structure might not be complete
        # value = self.value(system=system, direction=direction, flex_sys_dir=True)
        value = self.aspect_value(FAT_VAL, system=system or '', direction=direction or '', flex_sys_dir=True)
        if isinstance(value, NODE_TYPES):
            value.set_env(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)
        else:
            self.set_system_root_rec_idx(system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)
        return self

    def set_system_root_rec_idx(self, system: Optional[AspectKeyType] = None, direction: Optional[AspectKeyType] = None,
                                root_rec: Optional[Record] = None, root_idx: Optional[IdxPathType] = ()) -> '_Field':
        """ set the root record and index of the data structure where this :class:`_Field` instance is included.

        :param system:          system id (don't pass or pass None to leave unchanged).
        :param direction:       direction id (don't pass or pass None to leave unchanged).
        :param root_rec:        new root Record instance of this data structure (pass None to leave unchanged).
        :param root_idx:        root index to this node/Record instance (pass None to determine).
        :return:                self (this :class:`_Field` instance).
        """
        r_rec = self.root_rec()
        assert isinstance(r_rec, Record), "_Field.set_system_root_rec_idx() expects root record of Record type"  # mypy
        root_rec, root_idx = use_rec_default_root_rec_idx(r_rec, root_rec,
                                                          idx=self.root_idx(), root_idx=root_idx,
                                                          met="_Field.set_system_root_rec")
        system, direction = use_rec_default_sys_dir(root_rec, system, direction)

        self.set_root_rec(root_rec, system=system, direction=direction)
        if FAT_REC not in self._aspects or system or direction:
            self.set_root_rec(root_rec)     # ensure also root_rec for main/non-sys field value

        if root_idx:
            self.set_root_idx(root_idx, system=system, direction=direction)
            if FAT_RCX not in self._aspects or system or direction:
                self.set_root_idx(root_idx)

        return self

    # aspect specific methods ===============================================================================

    def aspect_exists(self, *aspect_types: AspectKeyType,
                      system: AspectKeyType = '', direction: AspectKeyType = '',
                      flex_sys_dir: Optional[bool] = False
                      ) -> Optional[AspectKeyType]:
        """ check if aspect exists and return full aspect key (including system/direction) if yes.

        :param aspect_types:    aspect types (dict key prefixes) to search for.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                the full aspect key of the first found aspect that is matching the
                                passed aspect type and optionally also the passed system and direction ids.
        :return:
        """
        if flex_sys_dir:
            key = self.find_aspect_key(*aspect_types, system=system, direction=direction)
        else:
            for aspect_type in aspect_types:
                key = aspect_key(aspect_type, system=system, direction=direction)
                if key in self._aspects:
                    break
            else:
                key = None
        return key

    def aspect_value(self, *aspect_types: AspectKeyType,
                     system: AspectKeyType = '', direction: AspectKeyType = '',
                     flex_sys_dir: Optional[bool] = False
                     ) -> Any:
        """

        :param aspect_types:    aspect types (dict key prefixes) to search for.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                the value of the first found aspect that is matching the passed aspect type and
                                optionally also the passed system and direction ids or None if not found.
        """
        key = self.aspect_exists(*aspect_types, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        if key:
            val = self._aspects.get(key)
        else:
            val = None
        return val

    def del_aspect(self, type_or_key: AspectKeyType, system: AspectKeyType = '', direction: AspectKeyType = '') -> Any:
        """ remove aspect from this field.

        :param type_or_key:     either FAT_* type or full key (including already the system and direction)-
        :param system:          system id string (if type_or_key is a pure FAT_* constant).
        :param direction:       direction string FAD_* constant (if type_or_key is a pure FAT_* constant).
        :return:                the aspect value of the removed aspect.
        """
        key = aspect_key(type_or_key, system=system, direction=direction)
        assert key not in (FAT_IDX, FAT_REC, FAT_RCX), "_Field main name and root Record/index cannot be removed"
        assert key != FAT_VAL or FAT_CAL in self._aspects, "_Field main value only deletable when calculator exists"
        return self._aspects.pop(key)

    def set_aspect(self, aspect_value: Any, type_or_key: AspectKeyType,
                   system: AspectKeyType = '', direction: AspectKeyType = '',
                   protect: bool = False, allow_values: bool = False) -> '_Field':
        """ set/change the value of an aspect identified by `type_or_key`, `system` and `direction`.

        :param aspect_value:    the value to set on the aspect.
        :param type_or_key:     either FAT_* type or full key (including already the system and direction)-
        :param system:          system id string (if type_or_key is a pure FAT_* constant).
        :param direction:       direction string FAD_* constant (if type_or_key is a pure FAT_* constant).
        :param protect:         pass True to prevent overwrite of already existing/set aspect value.
        :param allow_values:    pass True to allow change of field value aspect (:data:`FAT_VAL` aspect key).
        :return:                self (this :class:`_Field` instance).
        """
        key = aspect_key(type_or_key, system=system, direction=direction)
        msg = f"_Field.set_aspect({aspect_value}, {type_or_key}, {system}, {direction}, {protect}, {allow_values}): "
        assert not protect or key not in self._aspects, \
            msg + f"{key} already exists as {self._aspects[key]}, pass protect=True to overwrite"
        assert allow_values or not key.startswith(FAT_VAL), \
            msg + "pass allow_values=True or set values of _Field instances with the methods set_value() or set_val()"

        if aspect_value is None:
            self.del_aspect(key)
        else:
            assert key != FAT_IDX or isinstance(aspect_value, (tuple, list)) or not field_name_idx_path(aspect_value), \
                msg + f"digits cannot be used in system-less/generic field name '{aspect_value}'"
            self._aspects[key] = aspect_value
        return self

    def set_aspects(self, allow_values: bool = False, **aspects: Any) -> '_Field':
        """ set multiple aspects provided in `aspects`.

        :param allow_values:    pass True to allow change of field value aspect (:data:`FAT_VAL` aspect key).
        :param aspects:         dict of aspects where the dict key is the full/complete aspect key.
        :return:                self (this :class:`_Field` instance).
        """
        for key, data in aspects.items():
            if key.endswith(CALLABLE_SUFFIX):
                assert callable(data), \
                    f"_Field.set_aspects() expects callable for aspect {key} with the {CALLABLE_SUFFIX}-suffix"
                key = key[:-len(CALLABLE_SUFFIX)]
                data = data(self)
            self.set_aspect(data, key, allow_values=allow_values)
        return self

    def add_aspects(self, allow_values: bool = False, **aspects: Any) -> '_Field':
        """ add multiple aspects provided in `aspects`.

        :param allow_values:    pass True to allow change of field value aspect (:data:`FAT_VAL` aspect key).
        :param aspects:         dict of aspects where the dict key is the full/complete aspect key.
        :return:                self (this :class:`_Field` instance).
        """
        for key, data in aspects.items():
            # adding any other aspect to instance aspects w/o system/direction from kwargs
            self.set_aspect(data, key, protect=True, allow_values=allow_values)
        return self

    def name(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True) -> str:
        """ determine one of the names of this field.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :return:                main or system-specific name of this field.
        """
        return self.aspect_value(FAT_IDX, system=system, direction=direction, flex_sys_dir=flex_sys_dir)

    def del_name(self, system: AspectKeyType, direction: AspectKeyType = '') -> '_Field':
        """ remove system-specific name from this field.

        :param system:          system id (has to be non-empty system id).
        :param direction:       direction id (def='' stands for both directions).
        :return:                self (this :class:`_Field` instance).
        """
        assert system, "_Field.del_name() expects to pass at least a non-empty system"
        self.del_aspect(FAT_IDX, system=system, direction=direction)
        return self

    def has_name(self, name: str, selected_sys_dir: Optional[dict] = None) -> Optional[AspectKeyType]:
        """ check if this field has a name identical to the one passed in `name`.

        :param name:                name to search for.
        :param selected_sys_dir:    pass dict for to get back the system and direction ids of the found name.
        :return:                    full aspect key of the found name (including system/direction) or None if not found.
        """
        for asp_key, asp_val in self._aspects.items():
            if asp_key.startswith(FAT_IDX) and asp_val == name:
                if selected_sys_dir is not None:
                    selected_sys_dir['system'] = aspect_key_system(asp_key)
                    selected_sys_dir['direction'] = aspect_key_direction(asp_key)
                return asp_key
        return None

    def set_name(self, name: str, system: AspectKeyType = '', direction: AspectKeyType = '', protect: bool = False
                 ) -> '_Field':
        """ set/change one of the names of this field.

        :param name:            the new name of this field.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass True to prevent overwrite of already set/existing name.
        :return:                self (this :class:`_Field` instance).
        """
        self.set_aspect(name, FAT_IDX, system=system, direction=direction, protect=protect)
        if system:
            root_idx = self.root_idx(system=system, direction=direction)
            if root_idx and root_idx[-1] != name:
                self.set_root_idx(root_idx[:-1] + (name, ), system=system, direction=direction)
        return self

    def root_rec(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[Record]:
        """ determine and return root record of this field with given system and direction ids.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                root record instance or None if not set.
        """
        return self.aspect_value(FAT_REC, system=system, direction=direction, flex_sys_dir=True)

    def set_root_rec(self, rec: Record, system: AspectKeyType = '', direction: AspectKeyType = '') -> '_Field':
        """ set/change the root record of this field, system and direction.

        :param rec:             root record instance.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                self (this :class:`_Field` instance).
        """
        self.set_aspect(rec, FAT_REC, system=system, direction=direction)
        return self

    def root_idx(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> IdxPathType:
        """ return the root index of this field for the specified `system` and `direction` ids.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                root index of this field.
        """
        return self.aspect_value(FAT_RCX, system=system, direction=direction, flex_sys_dir=True) or ()

    def set_root_idx(self, idx_path: IdxPathType, system: AspectKeyType = '', direction: AspectKeyType = ''
                     ) -> '_Field':
        """ set/change the root record of this field, system and direction.

        :param idx_path:        root index for this field/system/direction.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                self (this :class:`_Field` instance).
        """
        self.set_aspect(idx_path, FAT_RCX, system=system, direction=direction)
        return self

    def calculator(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[FieldCallable]:
        """ return the calculation callable for this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                callable used for to calculate the value of this field or None if not set/exists/found.
        """
        return self.aspect_value(FAT_CAL, system=system, direction=direction)

    def set_calculator(self, calculator: FieldCallable, system: AspectKeyType = '', direction: AspectKeyType = '',
                       protect: bool = False) -> '_Field':
        """ set/change the field value calculator of this field, system and direction.

        :param calculator:      new callable used for to calculate the value of this field.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass True to prevent overwrite of already set/existing calculator callable.
        :return:                self (this :class:`_Field` instance).
        """
        self.set_aspect(calculator, FAT_CAL, system=system, direction=direction, protect=protect)
        if aspect_key(FAT_VAL, system=system, direction=direction) in self._aspects:
            self.del_aspect(FAT_VAL, system=system, direction=direction)
        return self

    def clear_val(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Any:
        """ return the initial field value (the clear value) of this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                the found clear/init value or None if not set/found.
        """
        return self.aspect_value(FAT_CLEAR_VAL, system=system, direction=direction)

    def set_clear_val(self, clr_val, system: AspectKeyType = '', direction: AspectKeyType = '') -> '_Field':
        """ set/change the clear/init value of this field, `system` and `direction`.

         :param clr_val:         new clear/init value of this field.
         :param system:          system id (def='' stands for the main/system-independent value).
         :param direction:       direction id (def='' stands for the main/system-independent value).
         :return:                self (this :class:`_Field` instance).
         """
        return self.set_aspect(clr_val, FAT_CLEAR_VAL, system=system, direction=direction)

    def _ensure_system_value(self, system: AspectKeyType, direction: AspectKeyType = '',
                             root_rec: Record = None, root_idx: IdxPathType = ()):
        """ check if a field value for the specified `system`/`direction` exists and if not then create it.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        """
        if not self.aspect_exists(FAT_VAL, system=system, direction=direction):
            self.set_value(Value(), system=system, direction=direction, root_rec=root_rec, root_idx=root_idx)

    def converter(self, system: AspectKeyType, direction: AspectKeyType = '') -> Optional[FieldValCallable]:
        """ return the converter callable for this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                callable used for to convert the field value between systems or None if not set.

        Separate system-specific representations of the field value can be (automatically) converted
        by specifying a converter callable aspect.
        """
        assert system != '', "_Field converter can only be retrieved for a given/non-empty system"
        return self.aspect_value(FAT_CNV, system=system, direction=direction)

    def set_converter(self, converter: FieldValCallable,
                      system: AspectKeyType, direction: AspectKeyType = '', protect: bool = True,
                      root_rec: Record = None, root_idx: IdxPathType = ()) -> '_Field':
        """ set/change the field value converter of this field, system and direction.

        :param converter:       new callable used for to convert the value of this field between systems.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass False to allow overwrite of already set converter callable.
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                self (this :class:`_Field` instance).
        """
        assert system != '', "_Field converter can only be set for a given/non-empty system"
        self._ensure_system_value(system, direction=direction, root_rec=root_rec, root_idx=root_idx)
        return self.set_aspect(converter, FAT_CNV, system=system, direction=direction, protect=protect)

    def convert(self, val: Any, system: AspectKeyType, direction: AspectKeyType) -> Any:
        """ convert field value from/onto system.

        :param val:             field value to convert.
        :param system:          system to convert from/onto.
        :param direction:       conversion direction (from or onto - see :data:`FAD_FROM` and :data:`FAD_ONTO`).
        :return:                converted field value.
        """
        converter = self.converter(system=system, direction=direction)
        if converter:
            assert callable(converter), f"converter of Field {self} for {direction}{system} is not callable"
            val = converter(self, val)
        return val

    def filterer(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[FieldCallable]:
        """ return the filter callable for this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                callable used for to filter this field/parent-record or None if not set.
        """
        return self.aspect_value(FAT_FLT, system=system, direction=direction)

    def set_filterer(self, filterer: FieldCallable,
                     system: AspectKeyType = '', direction: AspectKeyType = '', protect: bool = False
                     ) -> '_Field':
        """ set/change the filterer callable of this field, system and direction.

        :param filterer:        new callable used for to filter this field or the parent record.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass True to prevent overwrite of already set/existing filter callable.
        :return:                self (this :class:`_Field` instance).
        """
        return self.set_aspect(filterer, FAT_FLT, system=system, direction=direction, protect=protect)

    def sql_expression(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[str]:
        """ return the sql column expression for this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                sql column expression string if set or None if not set.
        """
        return self.aspect_value(FAT_SQE, system=system, direction=direction)

    def set_sql_expression(self, sql_expression: str,
                           system: AspectKeyType = '', direction: AspectKeyType = '', protect: bool = False
                           ) -> '_Field':
        """ set/change sql column expression of this field, system and direction.

        :param sql_expression:  new sql column expression used for to fetch associated db column of this field.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass True to prevent overwrite of already set/existing filter callable.
        :return:                self (this :class:`_Field` instance).
        """
        return self.set_aspect(sql_expression, FAT_SQE, system=system, direction=direction, protect=protect)

    def validator(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[FieldValCallable]:
        """ return the validation callable for this field, `system` and `direction`.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                validation callable if set or None if not set.
        """
        return self.aspect_value(FAT_CHK, system=system, direction=direction)

    def set_validator(self, validator: FieldValCallable,
                      system: AspectKeyType = '', direction: AspectKeyType = '', protect: bool = False,
                      root_rec: Record = None, root_idx: IdxPathType = ()) -> '_Field':
        """ set/change the field value validator of this field, system and direction.

        :param validator:       new callable used for to validate the value of this field, systems and direction.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param protect:         pass False to allow overwrite of already set converter callable.
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                self (this :class:`_Field` instance).
        """
        assert callable(validator), f"validator of Field {self} for {direction}{system} has to be callable"
        self._ensure_system_value(system, direction=direction, root_rec=root_rec, root_idx=root_idx)
        return self.set_aspect(validator, FAT_CHK, system=system, direction=direction, protect=protect)

    def validate(self, val: Any, system: AspectKeyType = '', direction: AspectKeyType = '') -> bool:
        """ validate field value for specified `system` and `direction`.

        :param val:             field value to validate (if ok to be set as new field value).
        :param system:          system id of new field value.
        :param direction:       direction id of new field value.
        :return:                True if `val` is ok to be set as new field value else False.
        """
        validator = self.validator(system=system, direction=direction)
        return not callable(validator) or validator(self, val)

    def append_record(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                      root_rec: Record = None, root_idx: IdxPathType = ()) -> Record:
        """ append new record to the :class:`Records` value of this field/system/direction.

        :param system:          system id of the field value to extend.
        :param direction:       direction id of the field value to extend.
        :param flex_sys_dir:    pass False to prevent fallback to system-independent value.
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                added/appended :class:`Record` instance.
        """
        msg = "_Field.append_record() expects "
        value = self.aspect_value(FAT_VAL, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
        assert isinstance(value, Records), msg + f"Records type in value {value} but got {type(value)}"
        r_rec = self.root_rec(system=system, direction=direction)
        assert isinstance(r_rec, Record), msg + f"root record of type Record, got {type(r_rec)}"    # mypy
        root_rec, root_idx = use_rec_default_root_rec_idx(r_rec, root_rec,
                                                          idx=self.root_idx(system=system, direction=direction),
                                                          root_idx=root_idx,
                                                          met="_Fields.append_record")
        assert isinstance(root_rec, Record), msg + f"root_rec of type Record, got {type(root_rec)}"
        return value.append_record(root_rec=root_rec, root_idx=root_idx)

    def clear_leaves(self, system: AspectKeyType = '', direction: AspectKeyType = '', flex_sys_dir: bool = True,
                     reset_lists: bool = True) -> '_Field':
        """ clear/reset field values and if reset_lists == True also Records/Values lists to one item.

        :param system:          system of the field value to clear, pass None for to clear all field values.
        :param direction:       direction of the field value to clear.
        :param flex_sys_dir:    if True then also clear field value if system is given and field has no system value.
        :param reset_lists:     if True/def then also clear Records/lists to one item.
        :return:                self (this _Field instance).
        """
        def _clr_val(_sys, _dir, _fsd):
            asp_val.clear_leaves(system=_sys, direction=_dir, flex_sys_dir=_fsd, reset_lists=reset_lists)
            clr_val = self.clear_val(system=_sys, direction=_dir)
            if clr_val is not None:
                self.set_val(clr_val, system=_sys, direction=_dir, flex_sys_dir=False)
                init_sys_dir.append((_sys, _dir))

        init_sys_dir: List[Tuple[str, str]] = list()
        if system is None and direction is None:
            for asp_key, asp_val in self._aspects.items():
                if asp_key.startswith(FAT_VAL):
                    _clr_val(aspect_key_system(asp_key), aspect_key_direction(asp_key), False)
        else:
            asp_val = self.aspect_value(FAT_VAL, system=system, direction=direction, flex_sys_dir=flex_sys_dir)
            if asp_val is not None:
                _clr_val(system, direction, flex_sys_dir)

        # finally set clear val for field value if field has no explicit value for the system of the clear val
        for asp_key, asp_val in self._aspects.items():
            if asp_key.startswith(FAT_CLEAR_VAL):
                system = aspect_key_system(asp_key)
                direction = aspect_key_direction(asp_key)
                if (system, direction) not in init_sys_dir:
                    self.set_val(asp_val, flex_sys_dir=False)

        return self

    def copy(self, deepness=0, root_rec: Record = None, root_idx: IdxPathType = (), **kwargs) -> '_Field':
        """ copy the aspects (names, indexes, values, ...) of this field.

        :param deepness:        deep copy level: <0==see deeper(), 0==only copy current instance, >0==deep copy
                                to deepness value - _Field occupies two deepness: 1st=_Field, 2nd=Value).
        :param root_rec:        destination root record.
        :param root_idx:        destination index path (tuple of field names and/or list/Records/Values indexes).
        :param kwargs:          additional arguments (will be passed on - most of them used by Record.copy).
        :return:                new/copied :class:`_Field` instance.
        """
        aspects = self._aspects
        if deepness:
            copied = dict()
            for asp_key, asp_val in aspects.items():
                if asp_key.startswith(FAT_VAL) and deeper(deepness, asp_val):
                    # FAT_VAL.asp_val is field value of VALUE_TYPES (Value, Records, ...)
                    copied[asp_key] = asp_val.copy(deepness=deeper(deepness, asp_val),
                                                   root_rec=root_rec, root_idx=root_idx, **kwargs)
                elif asp_key not in (FAT_REC, FAT_RCX):
                    copied[asp_key] = asp_val
            aspects = copied
        return _Field(root_rec=root_rec, root_idx=root_idx, allow_values=True, **aspects)

    def parent(self, system: AspectKeyType = '', direction: AspectKeyType = '',
               value_types: Optional[Tuple[Type[ValueType], ...]] = None) -> Optional[ValueType]:
        """ determine one of the parent ValueType instances in this data structure above of this field.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param value_types:     pass tuple of :data:`ValueType` for to restrict search to one of the passed types.
        :return:                found parent instance or None if not set or if type is not of passed `value_types`.
        """
        root_rec = self.root_rec(system=system, direction=direction)
        root_idx = self.root_idx(system=system, direction=direction)
        while root_rec and root_idx:
            root_idx = root_idx[:-1]
            if root_idx:
                item = root_rec.value(*root_idx, system=system, direction=direction)
                if not value_types or isinstance(item, value_types):
                    return item
        return root_rec if not value_types or isinstance(root_rec, value_types) else None

    def pull(self, from_system: AspectKeyType, root_rec: Record, root_idx: IdxPathType) -> '_Field':
        """ pull the system-specific value (specified by `from_system`) into the main value of this field.

        :param from_system:     system id of the system to pull from.
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                self (this _Field instance).
        """
        assert from_system, "_Field.pull() with empty value in from_system is not allowed"
        direction = FAD_FROM

        val = self.val(system=from_system, direction=direction)
        if val is None:
            val = ''
        if self.validate(val, from_system, direction):
            val = self.convert(val, from_system, direction)
            if val is not None:
                self.set_val(val, root_rec=root_rec, root_idx=root_idx)

        return self

    def push(self, onto_system: AspectKeyType, root_rec: Record, root_idx: IdxPathType) -> '_Field':
        """ push the main value of this field onto the system-specific value (specified by `onto_system`).

        :param onto_system:     system id of the system to pull from.
        :param root_rec:        root Record instance of this field, system and direction.
        :param root_idx:        root index to this node/:class:`_Field` instance.
        :return:                self (this _Field instance).
        """
        assert onto_system, "_Field.push() with empty value in onto_system is not allowed"
        direction = FAD_ONTO

        val = self.val()
        if val is None:
            val = ''
        val = self.convert(val, onto_system, direction)
        if val is not None and self.validate(val, onto_system, direction):
            self.set_val(val, system=onto_system, direction=direction, root_rec=root_rec, root_idx=root_idx)

        return self

    def string_to_records(self, str_val: str, field_names: Sequence, rec_sep: str = ',', fld_sep: str = '=',
                          system: AspectKeyType = '', direction: AspectKeyType = '') -> 'Records':
        """ convert formatted string into a :class:`Records` instance containing several :class:`Record` instances.

        :param str_val:         formatted string to convert.
        :param field_names:     list/tuple of field names of each record
        :param rec_sep:         character(s) used in `str_val` for to separate the records.
        :param fld_sep:         character(s) used in `str_val` for to separate the field values of each record.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                converted :class:`Records` instance.
        """
        fld_root_rec = self.root_rec(system=system, direction=direction)
        fld_root_idx = self.root_idx(system=system, direction=direction)

        return string_to_records(str_val, field_names, rec_sep=rec_sep, fld_sep=fld_sep,
                                 root_rec=fld_root_rec, root_idx=fld_root_idx)

    def record_field_val(self, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = ''
                         ) -> Any:
        """ get/determine the value of any field specified via `idx_path` within this data structure.

        :param idx_path:        index path of the field.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                the field value if found else None.

        This method has an alias named :meth:`.rfv`.
        """
        root_rec = self.root_rec(system=system, direction=direction)
        assert root_rec and idx_path, f"rfv() expects non-empty root_rec {root_rec} and idx_path {idx_path}"
        val = root_rec.val(*idx_path, system=system, direction=direction)
        return val

    rfv = record_field_val      #: alias of method :meth:`.record_field_val`

    def system_record_val(self, *idx_path: IdxItemType, system: AspectKeyType = '', direction: AspectKeyType = '',
                          use_curr_idx: Optional[list] = None) -> Any:
        """ get/determine the current value of a/this field within this data structure.

        :param idx_path:        index path of the field.
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :param use_curr_idx:    list of counters for to specify if and which current indexes have to be used.
        :return:                the currently selected field value if found else None.

        This method has an alias named :meth:`.srv`.
        """
        root_rec: Optional[Record] = self.root_rec(system=system, direction=direction)
        assert root_rec, f"srv() expects existing root_rec for system {system} and direction {direction}"
        if idx_path:
            field = root_rec.node_child(idx_path, use_curr_idx=use_curr_idx)
        else:
            field = self
        val = field.val(system=root_rec.system, direction=root_rec.direction) if field else None
        return val

    srv = system_record_val     #: alias of method :meth:`.system_record_val`

    def in_actions(self, *actions: str, system: AspectKeyType = '', direction: AspectKeyType = '') -> bool:
        """ determine if current data structure is in one of the passed `actions`.

        :param actions:         tuple of actions (see :data:`ACTION_` constants).
        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                True if the data structure has set one of the passed `actions` else False.

        This method has an alias named :meth:`.ina`.
        """
        root_rec = self.root_rec(system=system, direction=direction)
        is_in = root_rec is not None and root_rec.action in actions
        return is_in

    ina = in_actions            #: alias of method :meth:`.in_actions`

    def current_records_idx(self, system: AspectKeyType = '', direction: AspectKeyType = '') -> Optional[IdxItemType]:
        """ determine current index of :class:`Records` instance, situated above of this field in this data structure.

        :param system:          system id (def='' stands for the main/system-independent value).
        :param direction:       direction id (def='' stands for the main/system-independent value).
        :return:                full index path or None if no current index exists above this field.

        This method has an alias named :meth:`.crx`.
        """
        item = self.parent(system=system, direction=direction, value_types=(Records, ))
        if item:
            return get_current_index(cast(Records, item))
        return None

    crx = current_records_idx   #: alias of method :meth:`.current_records_idx`


VALUE_TYPES = (Value, Values, Record, Records)      #: tuple of classes/types used for system data values

# LIST_TYPES: Tuple[Type, ...] = (Values, Records)      -- typed tuple does not work in mypy with isinstance() restrict
LIST_TYPES = (Values, Records)                      #: tuple of classes/types used for system data lists
NODE_TYPES = (Record, Records)                      #: tuple of classes/types used for system data nodes
NODE_CHILD_TYPES = (_Field, Record)                 #: tuple of classes/types used for system data node children

# PARENT_TYPES = tuple(set(LIST_TYPES + NODE_TYPES))    -- does not work for mypy with isinstance() type restrict
PARENT_TYPES = (Values, Record, Records)            #: value types that can have children (Value excluded)
