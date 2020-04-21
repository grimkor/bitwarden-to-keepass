from bw_fetcher import BwFetcher
from kps_exporter import KpsImporter

bw_fetcher = BwFetcher()
kps_importer = KpsImporter()
kps_importer.set_target()
data = bw_fetcher.get_items()
kps_importer.import_list(data)
