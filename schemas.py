from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time


class SportCategorySchema(BaseModel):
    id: int
    name: str
    short_name: str | None = Field(alias="shortName")

    @field_validator("short_name", mode='before')
    def check_short_name(cls, value):
        if type(value) is int:
            return str(value)
        return value





class CountrySchema(BaseModel):
    id: int
    name: str




class RegionSchema(BaseModel):
    id: int
    name: str
    country: CountrySchema




class CitySchema(BaseModel):
    id: int
    name: str
    country: CountrySchema
    region: RegionSchema




class ClubSchema(BaseModel):
    id: int
    name: str

    @field_validator('name', mode='before')
    def check_type(cls, value):
        if type(value) is int:
            return str(value)
        return value




class GenderSchema(BaseModel):
    id: int
    name: str
    short_name: str = Field(alias="shortName")



class AthleteSchema(BaseModel):
    id: int
    name: str
    second_name: str | None = Field(alias="secondName")
    surname: str
    slug: str
    birth_year: int | None = Field(alias="birthYear")
    gender: GenderSchema
    sport_category: SportCategorySchema = Field(alias="sportCategory")
    city: CitySchema

    class Config:
        populate_by_name = True




class CheckpointSchema(BaseModel):
    id: int
    checkpoint_time: str = Field(alias="checkpointTime")
    start_time: str = Field(alias="startTime")




class ResultStatusSchema(BaseModel):
    id: int
    name: str
    description: str
    race_id: int | None
    race_distance_id: int | None




class ParticipantSchema(BaseModel):
    id: int
    athlete: AthleteSchema
    club: ClubSchema
    race_id: int = Field(alias="raceId")
    race_distance_id: int = Field(alias="raceDistanceId")
    race_number: int = Field(alias="raceNumber")
    race_time: str | None = Field(alias="raceTime")
    rating: float | None
    result_status: ResultStatusSchema = Field(alias="resultStatus")
    checkpoints: list[CheckpointSchema]


    class Config:
        populate_by_name = True




class DistanceSchema(BaseModel):
    ru: str
    en: str




class TitleSchema(BaseModel):
    ru: str
    en: str




class ProtocolSchema(BaseModel):
    title: TitleSchema
    distance: DistanceSchema
    race_id: int
    competition_id: int
    participants: list[ParticipantSchema]