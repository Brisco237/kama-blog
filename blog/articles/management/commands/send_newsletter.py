from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from ...models import Article, NewsletterSubscriber

class Command(BaseCommand):
    help = "Envoie la newsletter aux abonnés"

    def handle(self, *args, **kwargs):
        articles = Article.objects.order_by("-created_at")[:2]
        subscribers = NewsletterSubscriber.objects.all()

        if not articles.exists():
            self.stdout.write("Aucun article trouvé")
            return

        if not subscribers.exists():
            self.stdout.write("Aucun abonné")
            return

        for subscriber in subscribers:
            subject = "📰 Les derniers articles sur Kama-Blog"
            from_email = "Kama Blog <kamdembrice770@gmail.com>"
            to = [subscriber.email]

            # Construire la liste des articles
            articles_html = ""
            for article in articles:
                articles_html += f"""
                    <div style="background-color: #ffffff; border-radius: 10px; margin-bottom: 20px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: transform 0.3s ease;">
                        <div style="padding: 25px;">
                            <h3 style="color: #667eea; margin: 0 0 10px 0; font-size: 18px; font-weight: bold;">
                                {article.title}
                            </h3>
                            <p style="color: #999999; font-size: 13px; margin: 0 0 15px 0;">
                                📅 {article.created_at.strftime('%d %B %Y')}
                            </p>
                            <p style="color: #555555; margin: 0 0 20px 0; line-height: 1.6; font-size: 14px;">
                                {article.summary}
                            </p>
                            <a href="#" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px;">
                                Lire l'article →
                            </a>
                        </div>
                    </div>
                """

            html_content = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);">
                            
                            <!-- Header -->
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: bold;">📰 Derniers Articles</h1>
                                <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 14px;">Les nouvelles publications sur Kama-Blog</p>
                            </div>
                            
                            <!-- Main Content -->
                            <div style="padding: 40px 30px; color: #333333;">
                                <p style="font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                    Salut,
                                </p>
                                
                                <p style="font-size: 15px; line-height: 1.6; margin: 0 0 30px 0;">
                                    Voici les <strong>derniers articles</strong> publiés sur Kama-Blog. Ne les manquez pas ! 🔥
                                </p>
                                
                                <!-- Articles -->
                                <div style="margin: 0 0 30px 0;">
                                    {articles_html}
                                </div>
                                
                                <p style="font-size: 14px; line-height: 1.6; margin: 0 0 20px 0; color: #666666;">
                                    Merci de nous suivre et de rester connecté ! Si vous avez des suggestions ou des idées d'articles, n'hésitez pas à nous contacter. 😊
                                </p>
                            </div>
                            
                            <!-- Footer -->
                            <div style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="font-size: 14px; color: #999999; margin: 0 0 15px 0;">
                                    © 2026 Kama-Blog. Tous droits réservés.
                                </p>
                                <p style="font-size: 12px; color: #aaaaaa; margin: 0;">
                                    Vous recevez cet email parce que vous êtes abonné à la newsletter de Kama-Blog.
                                </p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            """

            msg = EmailMultiAlternatives(
                subject,
                "Découvrez les derniers articles sur Kama-Blog",
                from_email,
                to,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        self.stdout.write(self.style.SUCCESS("Newsletter envoyée aux abonnés ✅"))
