from sqlalchemy.orm.scoping import scoped_session
import json

import project
from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        data_filter = json.request

        status = data_filter.get('status')
        if status == 'new':
            movies = self._db_session.query(Movie).order_by(Movie.id.desc())

        page = data_filter.get('page')

        if page is not None:
            page_int = int(data_filter.get('page'))
            movies = movies.paginate(page_int,
                                     project.config.BaseConfig.ITEMS_PER_PAGE,
                                     False).items

            return movies
        else:
            return movies.all()
