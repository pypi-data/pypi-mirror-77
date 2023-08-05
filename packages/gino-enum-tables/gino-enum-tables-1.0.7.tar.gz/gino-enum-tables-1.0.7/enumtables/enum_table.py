import re
import sqlalchemy as sa

__all__ = ["EnumTable"]


def convert_case(name):
    s_1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s_1).lower()


def EnumTable(enum, base_gino_model, name=None, tablename=None, doc=None, **kwargs):
    """
	Create a table for a Python enumeration

	Parameters
	----------
	enum : subclass of enum.Enum
		The enumeration for which the table will be created.
	base_gino_model : GINO base model class
		The declarative base to use to create the enum class.
	name : str
		The name of the class to create, defaults to the name of the enum class with ``Table`` appended.
		For an enum class ``SpamEnum``, the default name would be ``SpamEnumTable``.
	tablename : str
		The name of the table in the database.
		Defaults to the name of the enum class converted to snake_case.
		WIth the example above, it would be ``spam_enum``.
	doc : str
		A docstring to add to the class.
		If left to ``None``, no docstring will be added.

	Additional keyword parameters become members of the class.

	Returns
	-------
	table : Model
		The table class, an subclass of ``Model``.
		The original enum is accissible as the ``__enum__`` attribute.
		It has one column, ``item_id`` of type String.
	"""

    typename = name if name else (enum.__name__ + "Table")
    namespace = {
        "__tablename__": tablename if tablename else convert_case(enum.__name__),
        "__enum__": enum,
        "item_id": sa.Column(sa.String, primary_key=True),
        **kwargs,
    }
    if doc:
        namespace["__doc__"] = doc
    return base_gino_model.__class__(typename, (base_gino_model,), namespace)
