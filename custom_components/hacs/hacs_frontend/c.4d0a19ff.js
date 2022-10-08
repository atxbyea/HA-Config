import{a as i,h as a,e as t,t as o,i as s,$ as e,D as r,j as n,A as l,r as d,n as c}from"./main-bfa41146.js";import"./c.c9ce972e.js";import"./c.bef52cd4.js";import"./c.8e28b461.js";i([c("dialog-box")],(function(i,a){return{F:class extends a{constructor(...a){super(...a),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[o()],key:"_params",value:void 0},{kind:"field",decorators:[s("ha-textfield")],key:"_textField",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i}},{kind:"method",key:"closeDialog",value:function(){var i,a;return!(null!==(i=this._params)&&void 0!==i&&i.confirmation||null!==(a=this._params)&&void 0!==a&&a.prompt)&&(!this._params||(this._dismiss(),!0))}},{kind:"method",key:"render",value:function(){if(!this._params)return e``;const i=this._params.confirmation||this._params.prompt;return e`
      <ha-dialog
        open
        ?scrimClickAction=${i}
        ?escapeKeyAction=${i}
        @closed=${this._dialogClosed}
        defaultAction="ignore"
        .heading=${e`${this._params.warning?e`<ha-svg-icon
              .path=${r}
              style="color: var(--warning-color)"
            ></ha-svg-icon> `:""}${this._params.title?this._params.title:this._params.confirmation&&this.hass.localize("ui.dialogs.generic.default_confirmation_title")}`}
      >
        <div>
          ${this._params.text?e`
                <p class=${this._params.prompt?"no-bottom-padding":""}>
                  ${this._params.text}
                </p>
              `:""}
          ${this._params.prompt?e`
                <ha-textfield
                  dialogInitialFocus
                  value=${n(this._params.defaultValue)}
                  .placeholder=${n(this._params.placeholder)}
                  .label=${this._params.inputLabel?this._params.inputLabel:""}
                  .type=${this._params.inputType?this._params.inputType:"text"}
                ></ha-textfield>
              `:""}
        </div>
        ${i&&e`
          <mwc-button @click=${this._dismiss} slot="secondaryAction">
            ${this._params.dismissText?this._params.dismissText:this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
        `}
        <mwc-button
          @click=${this._confirm}
          ?dialogInitialFocus=${!this._params.prompt}
          slot="primaryAction"
        >
          ${this._params.confirmText?this._params.confirmText:this.hass.localize("ui.dialogs.generic.ok")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_dismiss",value:function(){var i;null!==(i=this._params)&&void 0!==i&&i.cancel&&this._params.cancel(),this._close()}},{kind:"method",key:"_confirm",value:function(){var i;this._params.confirm&&this._params.confirm(null===(i=this._textField)||void 0===i?void 0:i.value);this._close()}},{kind:"method",key:"_dialogClosed",value:function(i){"ignore"!==i.detail.action&&this._dismiss()}},{kind:"method",key:"_close",value:function(){this._params&&(this._params=void 0,l(this,"dialog-closed",{dialog:this.localName}))}},{kind:"get",static:!0,key:"styles",value:function(){return d`
      :host([inert]) {
        pointer-events: initial !important;
        cursor: initial !important;
      }
      a {
        color: var(--primary-color);
      }
      p {
        margin: 0;
        color: var(--primary-text-color);
      }
      .no-bottom-padding {
        padding-bottom: 0;
      }
      .secondary {
        color: var(--secondary-text-color);
      }
      ha-dialog {
        --mdc-dialog-heading-ink-color: var(--primary-text-color);
        --mdc-dialog-content-ink-color: var(--primary-text-color);
        /* Place above other dialogs */
        --dialog-z-index: 104;
      }
      @media all and (min-width: 600px) {
        ha-dialog {
          --mdc-dialog-min-width: 400px;
        }
      }
      ha-textfield {
        width: 100%;
      }
    `}}]}}),a);
