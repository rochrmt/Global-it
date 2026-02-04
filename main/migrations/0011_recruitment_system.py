# Generated manually
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_candidature_remove_jobapplication_job_offer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OffreEmploi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200, verbose_name='Titre du poste')),
                ('description', models.TextField(verbose_name='Description du poste')),
                ('type_contrat', models.CharField(choices=[('cdi', 'CDI'), ('cdd', 'CDD'), ('stage', 'Stage'), ('alternance', 'Alternance'), ('freelance', 'Freelance')], default='cdi', max_length=20, verbose_name='Type de contrat')),
                ('lieu', models.CharField(max_length=200, verbose_name='Lieu de travail')),
                ('missions', models.TextField(verbose_name='Missions principales')),
                ('profil_recherche', models.TextField(verbose_name='Profil recherché')),
                ('experience_min', models.CharField(blank=True, help_text='Ex: 2 ans, Débutant accepté', max_length=100, verbose_name='Expérience minimale')),
                ('salaire_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salaire minimum (€)')),
                ('salaire_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Salaire maximum (€)')),
                ('date_debut', models.DateField(blank=True, null=True, verbose_name='Date de début souhaitée')),
                ('date_limite', models.DateField(blank=True, null=True, verbose_name='Date limite de candidature')),
                ('avantages', models.TextField(blank=True, help_text='Tickets restaurant, télétravail, etc.', verbose_name='Avantages')),
                ('image', models.ImageField(blank=True, help_text="Image de présentation de l'offre", null=True, upload_to='job_offers/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])),
                ('urgent', models.BooleanField(default=False, verbose_name='Recrutement urgent')),
                ('est_actif', models.BooleanField(default=True, verbose_name='Offre active')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
            ],
            options={
                'verbose_name': "Offre d'emploi",
                'verbose_name_plural': "Offres d'emploi",
                'ordering': ['-urgent', '-date_creation'],
            },
        ),
        migrations.CreateModel(
            name='CandidatureSpontanee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=100, verbose_name='Prénom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('poste_souhaite', models.CharField(max_length=200, verbose_name='Poste souhaité')),
                ('motivation', models.TextField(verbose_name='Lettre de motivation')),
                ('cv', models.FileField(help_text='Formats acceptés: PDF, DOC, DOCX (max 5MB)', upload_to='cv/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx'])], verbose_name='CV')),
                ('statut', models.CharField(choices=[('nouvelle', 'Nouvelle'), ('en_cours', "En cours d'examen"), ('acceptee', 'Acceptée'), ('rejetee', 'Rejetée')], default='nouvelle', max_length=20, verbose_name='Statut')),
                ('notes_admin', models.TextField(blank=True, help_text='Visibles uniquement par les administrateurs', verbose_name='Notes internes')),
                ('date_candidature', models.DateTimeField(auto_now_add=True, verbose_name='Date de candidature')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
            ],
            options={
                'verbose_name': 'Candidature spontanée',
                'verbose_name_plural': 'Candidatures spontanées',
                'ordering': ['-date_candidature'],
            },
        ),
        # Delete existing Candidature model if exists
        migrations.DeleteModel(
            name='Candidature',
        ),
        # Create new Candidature model linked to OffreEmploi
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=100, verbose_name='Prénom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('telephone', models.CharField(blank=True, max_length=20, verbose_name='Téléphone')),
                ('motivation', models.TextField(verbose_name='Lettre de motivation')),
                ('cv', models.FileField(help_text='Formats acceptés: PDF, DOC, DOCX (max 5MB)', upload_to='cv/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx'])], verbose_name='CV')),
                ('statut', models.CharField(choices=[('nouvelle', 'Nouvelle'), ('en_cours', "En cours d'examen"), ('acceptee', 'Acceptée'), ('rejetee', 'Rejetée')], default='nouvelle', max_length=20, verbose_name='Statut')),
                ('notes_admin', models.TextField(blank=True, help_text='Visibles uniquement par les administrateurs', verbose_name='Notes internes')),
                ('date_candidature', models.DateTimeField(auto_now_add=True, verbose_name='Date de candidature')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('offre_emploi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidatures', to='main.offreemploi', verbose_name="Offre d'emploi")),
            ],
            options={
                'verbose_name': 'Candidature',
                'verbose_name_plural': 'Candidatures',
                'ordering': ['-date_candidature'],
            },
        ),
    ]
