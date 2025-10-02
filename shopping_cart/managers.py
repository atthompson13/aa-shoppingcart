from django.db import models

class ItemRequestManager(models.Manager):
    def pending(self):
        return self.filter(status='pending')
    
    def claimed(self):
        return self.filter(status='claimed')
    
    def completed(self):
        return self.filter(status='completed')
    
    def claimable(self):
        return self.filter(status='pending', fulfiller__isnull=True)
    
    def claimable_for_user(self, user):
        return self.claimable().exclude(user=user)
    
    def user_claims(self, user):
        return self.filter(fulfiller=user, status__in=['claimed', 'contract_created', 'contract_accepted'])
    
    def active(self):
        return self.exclude(status__in=['completed', 'cancelled', 'expired'])
