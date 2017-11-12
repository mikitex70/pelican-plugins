from pelican import logger, signals
import logging


global tagsMustContainAnyOf # Article must have at least one of these tags to be generated, or no tags at all
global tagsMustNotContain   # Articles with these tags will not be generated


def myFilter(generator):
    if tagsMustContainAnyOf:
        for article in generator.articles:
            if hasattr(article, 'tags'):
                tagFound = False

                for t in article.tags:
                    if t in tagsMustContainAnyOf:
                        tagFound = True
                        break    # Found at least one required tag, article must be kept

                if not tagFound:
                    generator.articles.remove(article)
                    logger.info("Article %s skipped as not contains required tags" % article.title)
            else:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.warning("Article %s have no tags" % article.source_path)

    if tagsMustNotContain:
        for article in generator.articles:
            if hasattr(article, 'tags'):
                for t in article.tags:
                    if t in tagsMustNotContain:
                        generator.articles.remove(article)
                        logger.info("Article %s skipped because has tag %s" % (article.source_path, t))
                        break


def pelican_init(pelicanobj):
    global tagsMustContainAnyOf, tagsMustNotContain

    if 'TAGS_MUST_CONTAIN_ANY_OF' in pelicanobj.settings:
        tagsMustContainAnyOf = pelicanobj.settings['TAGS_MUST_CONTAIN_ANY_OF']
    else:
        tagsMustContainAnyOf = []

    if 'TAGS_MUST_NOT_CONTAIN' in pelicanobj.settings:
        tagsMustNotContain = pelicanobj.settings['TAGS_MUST_NOT_CONTAIN']
    else:
        tagsMustNotContain = []


def register():
    signals.initialized.connect(pelican_init)
    signals.article_generator_pretaxonomy.connect(myFilter)
