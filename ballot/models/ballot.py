"""
Ballot related models. Everything a voter needs to vote on.
Models are influenced from
http://votinginfoproject.github.io/vip-specification/
"""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from locality.models import ReverseLookupStringMixin


@python_2_unicode_compatible
class Ballot(models.Model):
    """
    A voter's ballot, containing all the BallotItems that the voter will vote
    on in the voting booth on election day.
    """
    date = models.DateField(help_text='The day of the election.', null=True,
                            default=None)  # None when auto-create; manual fix
    locality = models.ForeignKey('locality.Locality')

    @classmethod
    def from_date(cls, date, locality):
        """
        Find the best matching ballot to the given date.
        """
        ballot, _ = cls.objects.get_or_create(
            locality=locality)
        return ballot

    def __str__(self):
        return '%s election for %s' % (
            str(self.date), str(self.locality))

    class Meta:
        ordering = ('date', 'locality__name', 'locality__short_name')


@python_2_unicode_compatible
class BallotItem(models.Model, ReverseLookupStringMixin):
    """
    A single referendum or candidate office which appears on a voter's Ballot.
    """
    CONTEST_TYPES = (
        ('R', 'Referendum'),
        ('O', 'Office'),
    )
    contest_type = models.CharField(
        max_length=1, choices=CONTEST_TYPES,
        help_text='Office if the contest is for a person, referendum if '
                  'the contest is for an issue.')
    ballot = models.ForeignKey(Ballot, related_name='ballot_items')

    def __str__(self):
        return (ReverseLookupStringMixin.__str__(self))

    class Meta:
        ordering = ('ballot__date', 'ballot__locality__short_name',
                    'ballot__locality__name')


@python_2_unicode_compatible
class BallotItemSelection(models.Model, ReverseLookupStringMixin):
    """
    YES/NO to a referendum, or a candidate.

    This is a *conceptually* abstract class, but exists
    as a Django model so that finance can point to propositions
    and candidates equally.
    """
    ballot_item = models.ForeignKey('BallotItem')

    def __str__(self):
        return ReverseLookupStringMixin.__str__(self)

    class Meta:
        ordering = ('ballot_item__ballot__date',
                    'ballot_item__ballot__locality__short_name',
                    'ballot_item__ballot__locality__name')
