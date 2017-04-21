class ItemValidator(object):
	def is_valid(self, item):
		return (self._is_valid_id(item) and
				self._is_valid_name(item) and
				self._is_valid_tournament_id(item))

	def _is_valid_id(self, item):
		if "id" in item:
			return item["id"] >= 0

		return True

	def _is_valid_name(self, item):
		if "name" in item:
			return item["name"] != ""

		return True

	def _is_valid_tournament_id(self, item):
		if "tournament_id" in item:
			return item["tournament_id"] >= 0

		return True
