from ..orm.entity import Entity, Column

class Instrument(Entity):

  @staticmethod
  def _table():
    return "instruments"

  def __init__(
      self,
      id=None,
      name=None,
      long_name=None,
      uuid=None,
  ):
    self.__id = id
    self.__name = name
    self.__long_name = long_name
    self.__uuid = uuid

  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, value):
    self.__name = value

  @property
  def long_name(self):
    return self.__long_name

  @long_name.setter
  def long_name(self, value):
    self.__long_name = value

  @property
  def uuid(self):
    if self.__uuid:
      return self.__uuid.lower()
    return self.__uuid

  @uuid.setter
  def uuid(self, value):
    self.__uuid = value


  @classmethod
  def _columns(cls):
    return (
      Column("instrument_id", cls.id, id=True, sequence="instruments_seq"),
      Column("instrument_name", cls.name),
      Column("long_name", cls.long_name),
      Column("instrument_uuid", cls.uuid)
    )

