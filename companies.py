"""
Comprehensive Company Database for India
Organized by tier: High-tier (MNCs), Mid-tier (Established), Startups (Unicorns/Growth)
"""

# ============================================
# HIGH-TIER COMPANIES (MNCs & Large Corps)
# ============================================
HIGH_TIER_COMPANIES = {
    # Tech Giants
    "Google": "https://careers.google.com/jobs/results/",
    "Microsoft": "https://careers.microsoft.com/us/en/",
    "Amazon": "https://amazon.jobs/en/",
    "Apple": "https://www.apple.com/careers/in/",
    "Meta (Facebook)": "https://www.metacareers.com/jobs/",
    "Netflix": "https://jobs.netflix.com/",
    "Adobe": "https://careers.adobe.com/us/en/",
    "Oracle": "https://www.oracle.com/corporate/careers/",
    "IBM": "https://www.ibm.com/employment/",
    "Salesforce": "https://www.salesforce.com/company/careers/",
    "SAP": "https://jobs.sap.com/",
    "Intel": "https://jobs.intel.com/",
    "NVIDIA": "https://www.nvidia.com/en-us/about-nvidia/careers/",
    "Cisco": "https://jobs.cisco.com/",
    "VMware": "https://careers.vmware.com/",
    "Dell Technologies": "https://jobs.dell.com/",
    
    # Financial Services
    "Goldman Sachs": "https://www.goldmansachs.com/careers/",
    "JPMorgan Chase": "https://careers.jpmorgan.com/",
    "Morgan Stanley": "https://www.morganstanley.com/careers/",
    "Citi": "https://jobs.citi.com/",
    "American Express": "https://careers.americanexpress.com/",
    "Visa": "https://usa.visa.com/careers.html",
    "Mastercard": "https://careers.mastercard.com/",
    "PayPal": "https://careers.pypl.com/",
    
    # Consulting
    "McKinsey & Company": "https://www.mckinsey.com/careers/",
    "Boston Consulting Group": "https://careers.bcg.com/",
    "Bain & Company": "https://www.bain.com/careers/",
    "Deloitte": "https://www2.deloitte.com/global/en/careers.html",
    "PwC": "https://www.pwc.com/gx/en/careers.html",
    "EY": "https://careers.ey.com/",
    "Accenture": "https://www.accenture.com/in-en/careers",
    "KPMG": "https://home.kpmg/xx/en/home/careers.html",
    
    # E-commerce & Retail
    "Walmart": "https://careers.walmart.com/",
    "Target": "https://corporate.target.com/careers/",
    
    # Automotive & Manufacturing
    "Tesla": "https://www.tesla.com/careers/",
    "BMW": "https://www.bmwgroup.jobs/",
    "Mercedes-Benz": "https://www.mercedes-benz.com/en/careers/",
    
    # Other Tech
    "Twitter (X)": "https://careers.twitter.com/",
    "LinkedIn": "https://careers.linkedin.com/",
    "Uber": "https://www.uber.com/us/en/careers/",
    "Airbnb": "https://careers.airbnb.com/",
    "Spotify": "https://www.lifeatspotify.com/jobs/",
}

# ============================================
# MID-TIER COMPANIES (Established Indian & Growing MNCs)
# ============================================
MID_TIER_COMPANIES = {
    # Indian IT Services
    "TCS (Tata Consultancy Services)": "https://www.tcs.com/careers/",
    "Infosys": "https://www.infosys.com/careers/",
    "Wipro": "https://careers.wipro.com/",
    "HCL Technologies": "https://www.hcltech.com/careers/",
    "Tech Mahindra": "https://www.techmahindra.com/en-in/careers/",
    "LTI Mindtree": "https://www.ltimindtree.com/careers/",
    "Mphasis": "https://www.mphasis.com/home/careers.html",
    "Persistent Systems": "https://www.persistent.com/careers/",
    "Hexaware": "https://hexaware.com/careers/",
    "Cyient": "https://www.cyient.com/careers/",
    
    # Indian Product Companies
    "Flipkart": "https://www.flipkartcareers.com/",
    "Swiggy": "https://careers.swiggy.com/",
    "Zomato": "https://www.zomato.com/careers/",
    "Paytm (One97)": "https://paytm.com/careers/",
    "PhonePe": "https://www.phonepe.com/careers/",
    "Ola": "https://www.olacabs.com/careers/",
    "MakeMyTrip": "https://careers.makemytrip.com/",
    "Nykaa": "https://www.nykaa.com/careers",
    "PolicyBazaar": "https://www.policybazaar.com/about-us/careers/",
    "Razorpay": "https://razorpay.com/jobs/",
    "Freshworks": "https://www.freshworks.com/company/careers/",
    "Zoho": "https://www.zoho.com/careers/",
    "Postman": "https://www.postman.com/company/careers/",
    "BrowserStack": "https://www.browserstack.com/careers/",
    "Chargebee": "https://www.chargebee.com/company/careers/",
    
    # Fintech
    "CRED": "https://careers.cred.club/",
    "Groww": "https://groww.in/careers/",
    "Zerodha": "https://zerodha.com/careers/",
    "Upstox": "https://upstox.com/careers/",
    "Pine Labs": "https://www.pinelabs.com/careers/",
    
    # Edtech
    "BYJU'S": "https://jobs.byjus.com/",
    "Unacademy": "https://unacademy.com/careers/",
    "Vedantu": "https://www.vedantu.com/careers/",
    "upGrad": "https://www.upgrad.com/us/about-us/careers/",
    "Eruditus": "https://www.eruditus.com/careers/",
    
    # Emerging Tech
    "Sharechat": "https://sharechat.com/careers/",
    "Dream11": "https://www.dream11.com/careers/",
    "MPL (Mobile Premier League)": "https://www.mpl.live/careers/",
    "Urban Company": "https://www.urbancompany.com/careers/",
    "Meesho": "https://www.meesho.com/careers/",
    "Dunzo": "https://www.dunzo.com/careers/",
    "Delhivery": "https://www.delhivery.com/careers/",
    "BlackBuck": "https://blackbuck.com/careers/",
    "Rivigo": "https://rivigo.com/careers/",
    
    # Global Companies with Strong India Presence
    "Atlassian": "https://www.atlassian.com/company/careers/",
    "Snowflake": "https://careers.snowflake.com/",
    "Databricks": "https://www.databricks.com/company/careers/",
    "MongoDB": "https://www.mongodb.com/careers/",
    "Redis": "https://redis.com/company/careers/",
    "Elastic": "https://www.elastic.co/about/careers/",
    "Confluent": "https://www.confluent.io/careers/",
    "HashiCorp": "https://www.hashicorp.com/careers/",
    "GitLab": "https://about.gitlab.com/jobs/",
    "GitHub": "https://github.com/about/careers/",
    "Slack": "https://slack.com/careers/",
    "Twilio": "https://www.twilio.com/company/jobs/",
    "Stripe": "https://stripe.com/jobs/",
    "ServiceNow": "https://careers.servicenow.com/",
    "Workday": "https://www.workday.com/en-us/company/careers.html",
}

# ============================================
# STARTUPS (Unicorns & High-Growth)
# ============================================
STARTUP_COMPANIES = {
    # Unicorns & Soonicorns
    "Razorpay": "https://razorpay.com/jobs/",
    "Gupshup": "https://www.gupshup.io/company/careers/",
    "Innovaccer": "https://innovaccer.com/careers/",
    "Icertis": "https://www.icertis.com/company/careers/",
    "Mindtickle": "https://www.mindtickle.com/careers/",
    "Zenoti": "https://www.zenoti.com/careers/",
    "Postman": "https://www.postman.com/company/careers/",
    "Whatfix": "https://whatfix.com/careers/",
    "CleverTap": "https://clevertap.com/careers/",
    "Darwinbox": "https://darwinbox.com/careers/",
    "Ather Energy": "https://www.atherenergy.com/careers/",
    "Moglix": "https://www.moglix.com/careers/",
    "Licious": "https://www.licious.in/careers/",
    "Country Delight": "https://countrydelight.in/careers/",
    
    # High-Growth Startups
    "Polygon": "https://polygon.technology/careers/",
    "CoinDCX": "https://coindcx.com/careers/",
    "CoinSwitch": "https://coinswitch.co/careers/",
    "Spinny": "https://www.spinny.com/careers/",
    "Cars24": "https://www.cars24.com/careers/",
    "OYO": "https://www.oyorooms.com/careers/",
    "Practo": "https://www.practo.com/careers/",
    "Cure.fit": "https://www.cult.fit/careers/",
    "1mg": "https://www.1mg.com/careers/",
    "PharmEasy": "https://pharmeasy.in/careers/",
    "Pepperfry": "https://www.pepperfry.com/careers.html",
    "Lenskart": "https://www.lenskart.com/careers/",
    "BigBasket": "https://www.bigbasket.com/careers/",
    "Grofers (Blinkit)": "https://blinkit.com/careers/",
    "Udaan": "https://udaan.com/careers/",
    "Apna": "https://apna.co/careers/",
    "BharatPe": "https://bharatpe.com/careers/",
    "Jar": "https://www.jarapp.in/careers/",
    "Jupiter": "https://jupiter.money/careers/",
    "Fi Money": "https://fi.money/careers/",
    "Niyo": "https://www.goniyo.com/careers/",
    "Open": "https://open.money/careers/",
    
    # Deep Tech & AI Startups
    "Observe.AI": "https://www.observe.ai/careers/",
    "Haptik": "https://www.haptik.ai/careers/",
    "SigTuple": "https://sigtuple.com/careers/",
    "Niramai": "https://www.niramai.com/careers/",
    "Mad Street Den": "https://www.madstreetden.com/careers/",
    "Manthan (RichRelevance)": "https://www.richrelevance.com/careers/",
    "Niki.ai": "https://niki.ai/careers/",
    "Locus": "https://locus.sh/careers/",
    "Crayon Data": "https://crayondata.com/careers/",
    
    # Developer Tools & SaaS
    "Hasura": "https://hasura.io/careers/",
    "LambdaTest": "https://www.lambdatest.com/careers/",
    "BrowserStack": "https://www.browserstack.com/careers/",
    "TestSigma": "https://testsigma.com/careers/",
    "Appsmith": "https://www.appsmith.com/careers/",
    "Glific": "https://glific.org/careers/",
    "Frappe": "https://frappe.io/careers/",
    "Hoppscotch": "https://hoppscotch.io/careers/",
    
    # Gaming & Entertainment
    "Winzo": "https://www.winzogames.com/careers/",
    "Mobile Premier League (MPL)": "https://www.mpl.live/careers/",
    "Zupee": "https://www.zupee.com/careers/",
    "Rooter": "https://www.rooter.io/careers/",
    "Loco": "https://loco.gg/careers/",
    
    # Logistics & Supply Chain
    "Shiprocket": "https://www.shiprocket.in/careers/",
    "Loadshare": "https://www.loadshare.net/careers/",
    "ElasticRun": "https://www.elasticrun.com/careers/",
    "Shadowfax": "https://www.shadowfax.in/careers/",
    "Porter": "https://porter.in/careers/",
    
    # AgriTech
    "DeHaat": "https://www.dehaat.com/careers/",
    "Ninjacart": "https://www.ninjacart.com/careers/",
    "AgroStar": "https://agrostar.in/careers/",
    "Waycool": "https://www.waycool.in/careers/",
}

# ============================================
# CONSOLIDATED LIST
# ============================================
def get_all_companies():
    """Returns all companies in priority order (High -> Mid -> Startup)"""
    all_companies = {}
    all_companies.update(HIGH_TIER_COMPANIES)
    all_companies.update(MID_TIER_COMPANIES)
    all_companies.update(STARTUP_COMPANIES)
    return all_companies


def get_companies_by_tier(tier: str = "all"):
    """
    Get companies filtered by tier.
    
    Args:
        tier (str): 'high', 'mid', 'startup', or 'all'
    
    Returns:
        dict: Company name -> career page URL
    """
    tier = tier.lower()
    
    if tier == "high":
        return HIGH_TIER_COMPANIES
    elif tier == "mid":
        return MID_TIER_COMPANIES
    elif tier == "startup":
        return STARTUP_COMPANIES
    else:
        return get_all_companies()


def get_company_list_for_ui():
    """Returns a formatted list for UI dropdown"""
    companies = get_all_companies()
    return sorted(companies.keys())


if __name__ == "__main__":
    # Display statistics
    all_companies = get_all_companies()
    
    print("="*60)
    print("📊 COMPANY DATABASE STATISTICS")
    print("="*60)
    print(f"🏆 High-Tier Companies: {len(HIGH_TIER_COMPANIES)}")
    print(f"🏢 Mid-Tier Companies: {len(MID_TIER_COMPANIES)}")
    print(f"🚀 Startups: {len(STARTUP_COMPANIES)}")
    print(f"📋 Total Companies: {len(all_companies)}")
    print("="*60)
    
    print("\n🔝 Sample High-Tier Companies:")
    for i, company in enumerate(list(HIGH_TIER_COMPANIES.keys())[:5], 1):
        print(f"  {i}. {company}")
    
    print("\n🏢 Sample Mid-Tier Companies:")
    for i, company in enumerate(list(MID_TIER_COMPANIES.keys())[:5], 1):
        print(f"  {i}. {company}")
    
    print("\n🚀 Sample Startups:")
    for i, company in enumerate(list(STARTUP_COMPANIES.keys())[:5], 1):
        print(f"  {i}. {company}")
