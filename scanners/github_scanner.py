import re
from github import Github
from github.GithubException import GithubException
from config.settings import GITHUB_TOKEN, SECRET_PATTERNS, GITHUB_REPOS_LIMIT
from core.logger import setup_logger
from core.database import db

logger = setup_logger(__name__)

class GitHubScanner:
    def __init__(self):
        try:
            self.github = Github(GITHUB_TOKEN)
            logger.info("GitHub connected")
        except Exception as e:
            logger.error(f"Failed to connect to GitHub: {str(e)}")
            raise
    
    def search_stripe_keys(self):
        logger.info("Starting GitHub scan for Stripe keys...")
        
        keys_found = 0
        search_queries = [
            'sk_live_',
            'sk_test_',
            'stripe_api_key',
        ]
        
        for query in search_queries:
            try:
                logger.info(f"Searching for: {query}")
                results = self.github.search_code(query, sort='indexed', order='desc')
                
                result_count = 0
                for file in results:
                    if result_count >= GITHUB_REPOS_LIMIT:
                        break
                    
                    try:
                        content = file.decoded_content.decode('utf-8', errors='ignore')
                        found_keys = self._extract_keys(content, 'stripe')
                        
                        for key in found_keys:
                            db.add_exposed_key(
                                key_value=key,
                                key_type='Stripe Live/Test Key',
                                source='GitHub',
                                source_url=file.html_url,
                                risk_level='CRITICAL'
                            )
                            keys_found += 1
                        
                        result_count += 1
                    
                    except Exception as e:
                        logger.warning(f"Could not process file: {str(e)}")
                        continue
            
            except GithubException as e:
                logger.error(f"GitHub API error: {str(e)}")
                continue
        
        logger.info(f"Scan complete. Found {keys_found} exposed keys")
        return keys_found
    
    def _extract_keys(self, content, key_type):
        found_keys = []
        
        if key_type == 'stripe':
            patterns = [
                SECRET_PATTERNS.get('stripe_live'),
                SECRET_PATTERNS.get('stripe_test'),
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                found_keys.extend(matches)
        
        return list(set(found_keys))

def run_github_scan():
    try:
        scanner = GitHubScanner()
        scanner.search_stripe_keys()
    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")

if __name__ == '__main__':
    run_github_scan()
