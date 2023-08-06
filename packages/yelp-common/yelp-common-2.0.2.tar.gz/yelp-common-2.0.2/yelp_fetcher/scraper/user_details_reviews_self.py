import re
from collections import namedtuple
from typing import List

from yelp_fetcher.scraper.bs4_util import get_elements_by_classname
from yelp_fetcher.scraper.common import get_review_ids


class ScrapedReview(
    namedtuple("ScrapedReview", "biz_id biz_name biz_address review_id review_date")
):
    pass


USER_REVIEW_URL = "https://www.yelp.com/user_details_reviews_self?rec_pagestart={}&userid={}"
DATE_REGEX = re.compile(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}")


def get_user_details_reviews_self_url(user_id, page=0):
    page_start = page * 10
    return USER_REVIEW_URL.format(page_start, user_id)


def _sanitize_address_elem(elem):
    return elem.decode_contents().strip().replace("<br/>", " ")


def get_user_biz_reviews(page) -> List[ScrapedReview]:
    biz_elems = get_elements_by_classname(page, "biz-name")
    biz_ids = list(map(lambda elem: elem["href"].split("/")[-1], biz_elems))
    biz_names = list(map(lambda elem: elem.get_text(), biz_elems))
    biz_addresses = list(map(_sanitize_address_elem, page.find_all("address")))

    review_ids = get_review_ids(page)

    review_date_elems = get_elements_by_classname(page, "rating-qualifier")

    # Exclude dates from "Previous review"
    review_date_elems = filter(lambda e: "Previous review" not in e.get_text(), review_date_elems)

    review_dates = list(
        map(lambda e: re.search(DATE_REGEX, e.get_text()).group(), review_date_elems)
    )

    tups = zip(biz_ids, biz_names, biz_addresses, review_ids, review_dates)
    scraped_reviews = list(map(lambda tup: ScrapedReview(*tup), tups))
    return scraped_reviews
