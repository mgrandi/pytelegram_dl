from sqlalchemy import Column, Index, Integer, Unicode, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_repr import RepresentableBase

from sqlalchemy_utils import PhoneNumberType, ChoiceType

import telegram_dl.db_model_enums as tgdl_model_enums

CustomDeclarativeBase = declarative_base(cls=RepresentableBase)

class User(CustomDeclarativeBase):

    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)

    # telegram fields
    tg_user_id = Column(Integer)
    first_name = Column(Unicode(length=100))
    last_name = Column(Unicode(length=100))
    user_name = Column(Unicode(length=100))
    phone_number = Column(PhoneNumberType)


    # i don't really care about the status so i won't store it, or have a UserStatus type really
    # status = Column()

    # profile_photo = Column()
    outgoing_link = Column(ChoiceType(tgdl_model_enums.LinkStateEnum, impl=Integer))
    incoming_link = Column(ChoiceType(tgdl_model_enums.LinkStateEnum, impl=Integer))
    is_verified = Column(Boolean)
    is_support = Column(Boolean)
    restriction_reason = Column(Unicode(length=255))
    is_scam = Column(Boolean)
    have_access = Column(Boolean)

    user_type = Column(ChoiceType(tgdl_model_enums.UserTypeEnum, impl=Integer))

    language_code = Column(Unicode(length=20))

    __table_args__ = tuple(

        # FIXME: does this create an index, or do i need to create a
        # index as well as a unique constraint?
        UniqueConstraint("tg_user_id", name="UQ-user-tg_user_id"),
    )


class File(CustomDeclarativeBase):

    __tablename__ = "file"

    # this is combining `file`, `localFile` and `remoteFile`


    # our unique identifier
    file_id = Column(Integer, primary_key=True)

    # seems to be local to the user and a very low number, like `27`
    tg_file_id = Column(Integer)
    size = Column(Integer)
    expected_size = Column(Integer)

    ##########################
    # `localFile` fields
    ##########################

    # i don't think i really need anything from this object?

    ##########################
    # `remoteFile` fields
    ##########################

    # seems to be the unique identifier across all of telegram for the file. Example:
    # `AQADAQADRbYxG4UzzgIACFG4CjAABAIAA4UzzgIABJJVDmJhXyVcVUQAAhYE`
    # only seems to be 60 characters in practice, but lets be safe
    remote_file_id = Column(Unicode(100))


    __table_args__ = tuple(

        # FIXME: does this create an index, or do i need to create a
        # index as well as a unique constraint?
        UniqueConstraint("tg_file_id", name="UQ-file-tg_file_id")
    )


class ProfilePhoto(CustomDeclarativeBase):

    __tablename__ = "profile_photo"

    profile_photo_id = Column(Integer, primary_key=True)

    tg_profile_photo_id = Column(Integer)
    big_id = Column(Integer, ForeignKey("file.tg_file_id"))
    small_id = Column(Integer, ForeignKey("file.tg_file_id"))

    # see https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths
    big = relationship("File", foreign_keys=[big_id])
    small = relationship("File", foreign_keys=[small_id])

    __table_args__ = tuple(

        # FIXME: does this create an index, or do i need to create a
        # index as well as a unique constraint?
        UniqueConstraint("tg_profile_photo_id", name="UQ-profile_photo-tg_profile_photo_id")
    )




# class TEMPLATE(CustomDeclarativeBase):

#         __tablename__ = "SOMETHING"
#         __table_args__ = ( )