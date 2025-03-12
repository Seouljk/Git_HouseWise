from django.utils.timezone import now
from django.contrib.sessions.models import Session
from housewise.models import LoginSession

class SessionCleanupMiddleware:
    """
    Middleware to handle session cleanup for unexpected logouts
    and disconnections, such as app crashes or network issues.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Get the login session ID from the request session
                login_session_id = request.session.get('login_session_id')
                if login_session_id:
                    # Check if the session still exists
                    if not request.session.exists(request.session.session_key):
                        # Update the logout_time for unexpected session termination
                        login_session = LoginSession.objects.get(loginsession_id=login_session_id)
                        if not login_session.logout_time:  # Ensure logout_time is only set once
                            login_session.logout_time = now()
                            login_session.login_duration = login_session.logout_time - login_session.login_time
                            login_session.save()
            except LoginSession.DoesNotExist:
                # Login session does not exist; skip
                pass

        # Cleanup expired sessions
        self.cleanup_expired_sessions()

        return response

    @staticmethod
    def cleanup_expired_sessions():
        """
        Cleanup expired sessions and update logout time in LoginSession
        for those users whose sessions expired.
        """
        expired_sessions = Session.objects.filter(expire_date__lt=now())
        for session in expired_sessions:
            try:
                session_data = session.get_decoded()
                login_session_id = session_data.get('login_session_id')
                if login_session_id:
                    login_session = LoginSession.objects.get(loginsession_id=login_session_id)
                    if not login_session.logout_time:  # Ensure logout_time is only set once
                        login_session.logout_time = now()
                        login_session.login_duration = login_session.logout_time - login_session.login_time
                        login_session.save()
                session.delete()  # Delete the expired session
            except (LoginSession.DoesNotExist, KeyError):
                # LoginSession or session data not found; skip
                continue
