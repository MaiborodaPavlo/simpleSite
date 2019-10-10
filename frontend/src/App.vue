<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Content</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage" ></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.row-modal>Add Row</button>
        <br><br>
        <div class="container">
          <div class="large-12 medium-12 small-12 cell">
            <label>File
              <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
            </label>
              <button v-on:click="submitFile()">Submit</button>
          </div>
        </div>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">service_id</th>
              <th scope="col">servtype</th>
              <th scope="col">subtype</th>
              <th scope="col">user_id</th>
              <th scope="col">r_user_id</th>
              <th scope="col">state</th>
              <th scope="col">c_date</th>
              <th scope="col">c_time</th>
              <th scope="col">c_req_sent_date</th>
              <th scope="col">notified</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in data" :key="index">
              <td>{{ item.service_id }}</td>
              <td>{{ item.servtype }}</td>
              <td>{{ item.subtype }}</td>
              <td>{{ item.user_id }}</td>
              <td>{{ item.referrer_user_id }}</td>
              <td>{{ item.state }}</td>
              <td>{{ item.creation_date }}</td>
              <td>{{ item.creation_time }}</td>
              <td>{{ item.creation_request_sent_date }}</td>
              <td>{{ item.notified_about_expiration }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm"
                  v-b-modal.row-update-modal @click="editRow(item)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  @click="onDeleteRow(item)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
      <b-modal ref="addRowModal"
           id="row-modal"
           title="Add a new row"
           hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-service-id-group"
                    label="service_id:"
                    label-for="form-service-id-input">
          <b-form-input id="form-service-id-input"
                        type="text"
                        v-model="addRowForm.service_id"
                        required
                        placeholder="Enter service_id">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-servtype-group"
                      label="servtype:"
                      label-for="form-servtype-input">
            <b-form-input id="form-servtype-input"
                          type="text"
                          v-model="addRowForm.servtype"
                          required
                          placeholder="Enter servtype">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-subtype-group"
                      label="subtype:"
                      label-for="form-subtype-input">
            <b-form-input id="form-subtype-input"
                          type="text"
                          v-model="addRowForm.subtype"
                          required
                          placeholder="Enter subtype">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-user-id-group"
                      label="user_id:"
                      label-for="form-user-id-input">
            <b-form-input id="form-user-id-input"
                          type="text"
                          v-model="addRowForm.user_id"
                          required
                          placeholder="Enter user_id">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-referrer-user-id-group"
                      label="referrer_user_id:"
                      label-for="form-referrer-user-id-input">
            <b-form-input id="form-referrer-user-id-input"
                          type="text"
                          v-model="addRowForm.referrer_user_id"
                          required
                          placeholder="Enter referrer_user_id">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-state-group"
                      label="state:"
                      label-for="form-state-input">
            <b-form-input id="form-state-input"
                          type="text"
                          v-model="addRowForm.state"
                          required
                          placeholder="Enter state">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-date-group"
                      label="creation_date:"
                      label-for="form-creation-date-input">
            <b-form-input id="form-creation-date-input"
                          type="text"
                          v-model="addRowForm.creation_date"
                          required
                          placeholder="Enter creation_date">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-time-group"
                      label="creation_time:"
                      label-for="form-creation-time-input">
            <b-form-input id="form-creation-time-input"
                          type="text"
                          v-model="addRowForm.creation_time"
                          required
                          placeholder="Enter creation_time">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-request-sent-date-group"
                      label="creation_request_sent_date:"
                      label-for="form-creation-request-sent-date-input">
            <b-form-input id="form-creation-request-sent-date-input"
                          type="text"
                          v-model="addRowForm.creation_request_sent_date"
                          required
                          placeholder="Enter creation_request_sent_date">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-notified-about-expiration-group"
                      label="notified_about_expiration:"
                      label-for="form-notified-about-expiration-input">
            <b-form-input id="form-notified-about-expiration-input"
                          type="text"
                          v-model="addRowForm.notified_about_expiration"
                          required
                          placeholder="Enter notified_about_expiration">
            </b-form-input>
          </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editRowModal"
             id="row-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-servtype-edit-group"
                      label="servtype:"
                      label-for="form-servtype-edit-input">
            <b-form-input id="form-servtype-edit-input"
                          type="text"
                          v-model="editRowForm.servtype"
                          required
                          placeholder="Enter servtype">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-subtype-edit-group"
                      label="subtype:"
                      label-for="form-subtype-edit-input">
            <b-form-input id="form-subtype-edit-input"
                          type="text"
                          v-model="editRowForm.subtype"
                          required
                          placeholder="Enter subtype">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-user-id-edit-group"
                      label="user_id:"
                      label-for="form-user-id-edit-input">
            <b-form-input id="form-user-id-edit-input"
                          type="text"
                          v-model="editRowForm.user_id"
                          required
                          placeholder="Enter user_id">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-referrer-user-id-edit-group"
                      label="referrer_user_id:"
                      label-for="form-referrer-user-id-edit-input">
            <b-form-input id="form-referrer-user-id-edit-input"
                          type="text"
                          v-model="editRowForm.referrer_user_id"
                          required
                          placeholder="Enter referrer_user_id">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-state-edit-group"
                      label="state:"
                      label-for="form-state-edit-input">
            <b-form-input id="form-state-edit-input"
                          type="text"
                          v-model="editRowForm.state"
                          required
                          placeholder="Enter state">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-date-edit-group"
                      label="creation_date:"
                      label-for="form-creation-date-edit-input">
            <b-form-input id="form-creation-date-edit-input"
                          type="text"
                          v-model="editRowForm.creation_date"
                          required
                          placeholder="Enter creation_date">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-time-edit-group"
                      label="creation_time:"
                      label-for="form-creation-time-edit-input">
            <b-form-input id="form-creation-time-edit-input"
                          type="text"
                          v-model="editRowForm.creation_time"
                          required
                          placeholder="Enter creation_time">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-creation-request-sent-date-edit-group"
                      label="creation_request_sent_date:"
                      label-for="form-creation-request-sent-date-edit-input">
            <b-form-input id="form-creation-request-sent-date-edit-input"
                          type="text"
                          v-model="editRowForm.creation_request_sent_date"
                          required
                          placeholder="Enter creation_request_sent_date">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-notified-about-expiration-edit-group"
                      label="notified_about_expiration:"
                      label-for="form-notified-about-expiration-edit-input">
            <b-form-input id="form-notified-about-expiration-edit-input"
                          type="text"
                          v-model="editRowForm.notified_about_expiration"
                          required
                          placeholder="Enter notified_about_expiration">
            </b-form-input>
          </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Update</b-button>
          <b-button type="reset" variant="danger">Cancel</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>


<script>
import axios from 'axios';
import Alert from './components/Alert.vue';

const host = process.env.VUE_APP_BACKEND_HOST;

export default {
  data() {
    return {
      data: [],
      file: '',
      addRowForm: {
        service_id: '',
        servtype: '',
        subtype: '',
        user_id: '',
        referrer_user_id: '',
        state: '',
        creation_date: '',
        creation_time: '',
        creation_request_sent_date: '',
        notified_about_expiration: '',
      },
      editRowForm: {
        service_id: '',
        servtype: '',
        subtype: '',
        user_id: '',
        referrer_user_id: '',
        state: '',
        creation_date: '',
        creation_time: '',
        creation_request_sent_date: '',
        notified_about_expiration: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getData() {
      const path = `${host}/content`;
      axios.get(path)
        .then((res) => {
          this.data = res.data.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    submitFile() {
      const formData = new FormData();
      console.log(this.file);
      formData.append('file', this.file);
      const path = `${host}/content/upload`;
      axios.post(path, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((res) => {
          this.getData();
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getData();
        });
    },
    addRow(bodyFormData) {
      const path = `${host}/content`;
      axios.post(path, bodyFormData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((res) => {
          this.getData();
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getData();
        });
    },
    updateRow(itemID, bodyFormDataEdit) {
      const path = `${host}/content/${itemID}`;

      axios.put(path, bodyFormDataEdit)
        .then((res) => {
          this.getData();
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    editRow(item) {
      this.editRowForm = item;
    },
    initForm() {
      this.addRowForm.service_id = '';
      this.addRowForm.servtype = '';
      this.addRowForm.subtype = '';
      this.addRowForm.user_id = '';
      this.addRowForm.referrer_user_id = '';
      this.addRowForm.state = '';
      this.addRowForm.creation_date = '';
      this.addRowForm.creation_time = '';
      this.addRowForm.creation_request_sent_date = '';
      this.addRowForm.notified_about_expiration = '';
      this.editRowForm.service_id = '';
      this.editRowForm.servtype = '';
      this.editRowForm.subtype = '';
      this.editRowForm.user_id = '';
      this.editRowForm.referrer_user_id = '';
      this.editRowForm.state = '';
      this.editRowForm.creation_date = '';
      this.editRowForm.creation_time = '';
      this.editRowForm.creation_request_sent_date = '';
      this.editRowForm.notified_about_expiration = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addRowModal.hide();
      const bodyFormData = new FormData();
      bodyFormData.set('service_id', this.addRowForm.service_id);
      bodyFormData.set('servtype', this.addRowForm.servtype);
      bodyFormData.set('subtype', this.addRowForm.subtype);
      bodyFormData.set('user_id', this.addRowForm.user_id);
      bodyFormData.set('referrer_user_id', this.addRowForm.referrer_user_id);
      bodyFormData.set('state', this.addRowForm.state);
      bodyFormData.set('creation_date', this.addRowForm.creation_date);
      bodyFormData.set('creation_time', this.addRowForm.creation_time);
      bodyFormData.set('creation_request_sent_date', this.addRowForm.creation_request_sent_date);
      bodyFormData.set('notified_about_expiration', this.addRowForm.notified_about_expiration);

      this.addRow(bodyFormData);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addRowModal.hide();
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editRowModal.hide();
      const bodyFormDataEdit = new FormData();
      bodyFormDataEdit.set('service_id', this.editRowForm.service_id);
      bodyFormDataEdit.set('servtype', this.editRowForm.servtype);
      bodyFormDataEdit.set('subtype', this.editRowForm.subtype);
      bodyFormDataEdit.set('user_id', this.editRowForm.user_id);
      bodyFormDataEdit.set('referrer_user_id', this.editRowForm.referrer_user_id);
      bodyFormDataEdit.set('state', this.editRowForm.state);
      bodyFormDataEdit.set('creation_date', this.editRowForm.creation_date);
      bodyFormDataEdit.set('creation_time', this.editRowForm.creation_time);
      bodyFormDataEdit.set('creation_request_sent_date', this.editRowForm.creation_request_sent_date);
      bodyFormDataEdit.set('notified_about_expiration', this.editRowForm.notified_about_expiration);

      this.updateRow(this.editRowForm.service_id, bodyFormDataEdit);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editRowModal.hide();
      this.initForm();
      this.getData();
    },
    removeRow(itemID) {
      const path = `${host}/content/${itemID}`;
      axios.delete(path)
        .then((res) => {
          this.getData();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    onDeleteRow(item) {
      this.removeRow(item.service_id);
    },
  },
  created() {
    this.getData();
  },
};
</script>
