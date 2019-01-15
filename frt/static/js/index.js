let formModel = function () {
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
	self.title = ko.observable(undefined).extend({ required: true });
	self.description = ko.observable(undefined).extend({ required: true });
	self.selected_client = ko.observable(undefined).extend({ required: true });
	self.selected_priority = ko.observable(undefined).extend({ required: true, number: true });
	self.selected_area = ko.observable(undefined).extend({ required: true });
	self.deadline = ko.observable(getTodaysDate()).extend({ required: true });
	self.request_successful = ko.observable(null);
	self.request_failed = ko.observable(null);

	self.selected_client.subscribe(newClient => {
		self.fetch_priorities(newClient);
	});

	self.fetch_priorities = client => {
		if (client != undefined) {
			$.ajax(`/filter_priorities/${client}`, {
				method: 'GET',
				dataType: 'JSON',
				success: data => {
					self.priorities(data);
					self.selected_priority(data[0]);
				}
			});
		}
	};

	self.request_successful_toggle = () => {
		if (self.request_successful()) {
			self.request_successful(null);
		} else {
			self.request_successful(true);
			setTimeout(function () {
				self.request_successful(null);
			}, 4000);
		}
	}

	self.request_failed_toggle = () => {
		if (self.request_failed()) {
			self.request_failed(null);
		} else {
			self.request_failed(true);
			setTimeout(() => {
				self.request_failed(null);
			}, 4000);
		}
	}

	self.request_validation_errors = ko.validation.group({
		title: self.title,
		description: self.description,
		selected_client: self.selected_client,
		selected_priority: self.selected_priority,
		selected_area: self.selected_area,
		deadline: self.deadline
	})

	self.validte_request = () => {
		form_items = {
			title: self.title.isValid(),
			description: self.description.isValid(),
			selected_client: self.selected_client.isValid(),
			selected_priority: self.selected_priority.isValid(),
			selected_area: self.selected_area.isValid(),
			deadline: self.deadline.isValid()
		}
		for (item in form_items) {
			if (form_items.hasOwnProperty(item) && (!form_items[item])) {
				return false;
			}
		}
		return true;
	}

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
		if (self.validte_request()) {
			$.ajax('/api/v1/feature', {
				method: 'POST',
				contentType: 'application/json',
				data: ko.toJSON(self.post_payload()),

				success: () => {
					self.refresh();
					self.title(null);
					self.description(null);
					self.selected_client(undefined);
					self.selected_priority(undefined);
					self.selected_area(undefined);
					self.deadline(null);

					self.title.isModified(false);
					self.description.isModified(false);
					self.selected_client.isModified(false);
					self.selected_priority.isModified(false);
					self.selected_area.isModified(false);
					self.deadline.isModified(false);

					self.request_successful_toggle(true);
				},

				error: () => {
					self.request_failed_toggle(true);
				}
			});
		} else {
			self.request_validation_errors.showAllMessages(true);
		}
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
			success: () => {
				$(`#${feature_id}`).fadeOut(700, () => {
					$(this).remove();
					self.refresh();
				});
			}
		});
	};
};

getTodaysDate = () => {
	let today = new Date()
	let currentMonthPadded = ('0' + (today.getMonth() + 1)).slice(-2)
	return `${today.getFullYear()}-${currentMonthPadded}-${today.getDate()}`
}

let fm = new formModel();
ko.applyBindings(fm);
fm.refresh();

flatpickr('#deadline', {
	"disableMobile": true,
	"minDate": "today",
	"defaultDate": "today"
});