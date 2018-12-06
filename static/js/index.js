var FeatureModel = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, self);
};

let formModel = function() {
	let self = this;

	// Set dropdown options
	self.clients = ko.observableArray(['Client A', 'Client B', 'Client C']);
	self.priorities = ko.observableArray(undefined);
	self.areas = ko.observableArray([
		'Billing',
		'Claims',
		'Policies',
		'Reports'
	]);

	// Get form imput data
	self.title = ko.observable('');
	self.description = ko.observable('');
	self.selected_client = ko.observable(undefined);
	self.selected_priority = ko.observable(undefined);
	self.selected_area = ko.observable('');
	self.deadline = ko.observable('');

	self.selected_client.subscribe(newClient => {
		self.fetch_priorities(newClient);
	});

	self.fetch_priorities = client => {
		if (client != undefined) {
			$.ajax(`/filter_priorities/${client}`, {
				method: 'GET',
				dataType: 'JSON',
				success: function(data) {
					self.priorities(data);
					self.selected_priority(data[0]);
				}
			});
		}
	};

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

	self.delete = element => {
		feature_id = element.id;
		self.refresh();
		$.ajax(`/api/v1/feature/${feature_id}`, {
			method: 'DELETE',
			dataType: 'text',
			success: function() {
				$(`#${feature_id}`).fadeOut(700, () => {
					$(this).remove();
					self.refresh();
				});
			}
		});
	};
};

let fm = new formModel();
ko.applyBindings(fm);
fm.refresh();
