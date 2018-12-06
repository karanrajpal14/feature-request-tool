var FeatureModel = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, self);
};

let formModel = function() {
	let self = this;

	// Set dropdown options
	self.clients = ko.observableArray(['Client A', 'Client B', 'Client C']);
	self.priorities = ko.observableArray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
	self.areas = ko.observableArray([
		'Billing',
		'Claims',
		'Policies',
		'Reports'
	]);

	// Get form imput data
	self.title = ko.observable('');
	self.description = ko.observable('');
	self.selected_client = ko.observable('');
	self.selected_priority = ko.observable('');
	self.selected_area = ko.observable('');
	self.deadline = ko.observable('');

	// DEV
	self.title = ko.observable('OnePlus 9');
	self.description = ko.observable('One');
	self.selected_client = ko.observable('Client A');
	self.selected_priority = ko.observable(1);
	self.selected_area = ko.observable('Billing');
	self.deadline = ko.observable('2018-12-1');

	// amalgamate form inputs for POST body
	self.post_payload = ko.pureComputed(() => {
		return {
			title: self.title(),
			description: self.description(),
			client: self.selected_client(),
			priority: self.selected_priority(),
			product_area: self.selected_area(),
			deadline: self.deadline()
		};
	}, self);

	// make feature request
	self.save_form_input = () => {
		$.ajax('/api/v1/feature', {
			method: 'POST',
			contentType: 'application/json',
			data: ko.toJSON(self.post_payload()),

			success: (data, status) => {
				self.refresh();
			}
		});
	};

	self.get_all_feature_requests = ko.observableArray([]);

	self.refresh = () => {
		$.ajax('/api/v1/feature', {
			method: 'GET',
			dataType: 'JSON',
			success: self.get_all_feature_requests
		});
	};
};

let fm = new formModel();
ko.applyBindings(fm);
fm.refresh();
