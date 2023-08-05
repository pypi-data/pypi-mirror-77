# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.testimony


class CollectiveTestimonyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.testimony)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.testimony:default')


COLLECTIVE_TESTIMONY_FIXTURE = CollectiveTestimonyLayer()


COLLECTIVE_TESTIMONY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TESTIMONY_FIXTURE,),
    name='CollectiveTestimonyLayer:IntegrationTesting',
)


COLLECTIVE_TESTIMONY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TESTIMONY_FIXTURE,),
    name='CollectiveTestimonyLayer:FunctionalTesting',
)


COLLECTIVE_TESTIMONY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TESTIMONY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveTestimonyLayer:AcceptanceTesting',
)
