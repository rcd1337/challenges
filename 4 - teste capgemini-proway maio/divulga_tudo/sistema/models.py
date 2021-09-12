from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"(id: {self.id}) (name: {self.name}) (created_on: {self.created_on}"

class Ad(models.Model):
    name = models.CharField(max_length=255, blank=False)
    client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name="ads")
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    days = models.IntegerField(blank=False)
    investment_day = models.DecimalField(max_digits=12, decimal_places=2, blank=False)
    investment_total = models.DecimalField(max_digits=14, decimal_places=2, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"""(id: {self.id}) (name: {self.name}) (client: {self.client.name}) 
        (start: {self.start_date}) (end: {self.end_date}) (days: {self.days})
        (investment/day: {self.investment_day}) (investment_total: {self.investment_total})"""